import argparse
import logging
import os
import re
import torch
import torchaudio
import faster_whisper
from ctc_forced_aligner import (
    generate_emissions,
    get_alignments,
    get_spans,
    load_alignment_model,
    postprocess_results,
    preprocess_text,
)
from deepmultilingualpunctuation import PunctuationModel
from nemo.collections.asr.models.msdd_models import NeuralDiarizer
from helpers import (
    cleanup,
    create_config,
    find_numeral_symbol_tokens,
    get_realigned_ws_mapping_with_punctuation,
    get_sentences_speaker_mapping,
    get_words_speaker_mapping,
    langs_to_iso,
    process_language_arg,
    punct_model_langs,
    whisper_langs,
    write_srt,
)

mtypes = {"cpu": "int8", "cuda": "float16"}

def parse_arguments():
    """ Parse command-line arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--audio", help="name of the target audio file", required=True
    )
    parser.add_argument(
        "--no-stem",
        action="store_false",
        dest="stemming",
        default=True,
        help="Disables source separation. Helps with long files without music."
    )
    parser.add_argument(
        "--suppress_numerals",
        action="store_true",
        dest="suppress_numerals",
        default=False,
        help="Suppresses Numerical Digits."
    )
    parser.add_argument(
        "--whisper-model",
        dest="model_name",
        default="medium.en",
        help="name of the Whisper model to use",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        dest="batch_size",
        default=8,
        help="Batch size for inference, reduce if out of memory, set to 0 for original whisper longform inference",
    )
    parser.add_argument(
        "--language",
        type=str,
        default=None,
        choices=whisper_langs,
        help="Language spoken in the audio, specify None to perform language detection",
    )
    parser.add_argument(
        "--device",
        dest="device",
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="Use 'cuda' if you have a GPU, otherwise 'cpu'",
    )
    return parser.parse_args()

def isolate_vocals(audio_path, use_stem=True):
    """ Isolate vocals from the rest of the audio using Demucs """
    if use_stem:
        return_code = os.system(
            f'python -m demucs.separate -n htdemucs --two-stems=vocals "{audio_path}" -o temp_outputs'
        )
        if return_code != 0:
            logging.warning("Source splitting failed, using original audio file.")
            return audio_path
        return os.path.join("temp_outputs", "htdemucs", os.path.splitext(os.path.basename(audio_path))[0], "vocals.wav")
    else:
        return audio_path

def transcribe_audio(audio_waveform, model_name, device, batch_size, language, suppress_numerals):
    """ Transcribe audio file using Whisper model """
    whisper_model = faster_whisper.WhisperModel(model_name, device=device, compute_type=mtypes[device])
    whisper_pipeline = faster_whisper.BatchedInferencePipeline(whisper_model)
    suppress_tokens = find_numeral_symbol_tokens(whisper_model.hf_tokenizer) if suppress_numerals else [-1]

    if batch_size > 0:
        transcript_segments, info = whisper_pipeline.transcribe(
            audio_waveform, language, suppress_tokens=suppress_tokens, batch_size=batch_size
        )
    else:
        transcript_segments, info = whisper_model.transcribe(
            audio_waveform, language, suppress_tokens=suppress_tokens, vad_filter=True
        )

    full_transcript = "".join(segment.text for segment in transcript_segments)
    return full_transcript, info

def forced_alignment(audio_waveform, full_transcript, device, batch_size):
    """ Perform forced alignment using the CTC forced aligner """
    alignment_model, alignment_tokenizer = load_alignment_model(
        device, dtype=torch.float16 if device == "cuda" else torch.float32
    )

    emissions, stride = generate_emissions(
        alignment_model,
        torch.from_numpy(audio_waveform).to(alignment_model.dtype).to(alignment_model.device),
        batch_size=batch_size,
    )

    tokens_starred, text_starred = preprocess_text(full_transcript, romanize=True, language=langs_to_iso['en'])
    segments, scores, blank_token = get_alignments(emissions, tokens_starred, alignment_tokenizer)
    spans = get_spans(tokens_starred, segments, blank_token)
    word_timestamps = postprocess_results(text_starred, spans, stride, scores)
    
    return word_timestamps

def diarize_audio(audio_waveform, device):
    """ Perform diarization using NeMo's NeuralDiarizer """
    temp_path = os.path.join(os.getcwd(), "temp_outputs")
    os.makedirs(temp_path, exist_ok=True)
    
    torchaudio.save(
        os.path.join(temp_path, "mono_file.wav"),
        torch.from_numpy(audio_waveform).unsqueeze(0).float(),
        16000,
        channels_first=True,
    )

    msdd_model = NeuralDiarizer(cfg=create_config(temp_path)).to(device)
    msdd_model.diarize()

    speaker_ts = []
    with open(os.path.join(temp_path, "pred_rttms", "mono_file.rttm"), "r") as f:
        lines = f.readlines()
        for line in lines:
            line_list = line.split(" ")
            s = int(float(line_list[5]) * 1000)
            e = s + int(float(line_list[8]) * 1000)
            speaker_ts.append([s, e, int(line_list[11].split("_")[-1])])

    return speaker_ts

def postprocess_punctuation(wsm, language):
    """ Restore punctuation in the transcript """
    if language in punct_model_langs:
        punct_model = PunctuationModel(model="kredor/punctuate-all")
        words_list = list(map(lambda x: x["word"], wsm))
        labled_words = punct_model.predict(words_list, chunk_size=230)

        ending_puncts = ".?!"
        model_puncts = ".,;:!?."
        
        is_acronym = lambda x: re.fullmatch(r"\b(?:[a-zA-Z]\.){2,}", x)
        for word_dict, labeled_tuple in zip(wsm, labled_words):
            word = word_dict["word"]
            if word and labeled_tuple[1] in ending_puncts and (word[-1] not in model_puncts or is_acronym(word)):
                word += labeled_tuple[1]
                if word.endswith(".."):
                    word = word.rstrip(".")
                word_dict["word"] = word
    else:
        logging.warning(f"Punctuation restoration not available for {language} language.")
    
    return get_realigned_ws_mapping_with_punctuation(wsm)


def diarization_pipeline(audio_path, args):
    """ Full diarization pipeline that returns the ssm """
    # Step 1: Isolate vocals if needed
    vocal_target = isolate_vocals(audio_path, True)

    # Step 2: Transcribe the audio using Whisper
    audio_waveform = faster_whisper.decode_audio(vocal_target)
    full_transcript, info = transcribe_audio(audio_waveform, args['model_name'], args['device'], args['batch_size'], process_language_arg(args['language'], args['model_name']), args['suppress_numerals'])

    # Step 3: Forced Alignment
    word_timestamps = forced_alignment(audio_waveform, full_transcript, args['device'], args['batch_size'])

    # Step 4: Perform Diarization
    speaker_ts = diarize_audio(audio_waveform, args['device'])

    # Step 5: Align words with speaker timestamps
    wsm = get_words_speaker_mapping(word_timestamps, speaker_ts, "start")
    wsm = postprocess_punctuation(wsm, info.language)
    ssm = get_sentences_speaker_mapping(wsm, speaker_ts)


    # Step 7: Clean up
    cleanup("temp_outputs")

    # Return the speaker-aware sentences mapping (ssm)
    return ssm
