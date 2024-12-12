from setuptools import setup, find_packages

setup(
    name='knorket_diarize',
    version='0.1.0',
    author='ockhamlabs',
    author_email='hello@ockhamlabs.ai',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'knorket-diarize = knorket_diarize.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
       install_requires=[
        'requests',
        'pylint',
        'pylint-exit',
        'pyinstaller',
        'tqdm',
        'psutil',
        'packaging',
        'pyjwt',
        'colorama',
        'jinja2',
        'distro',
        'pyyaml',
        # Add more dependencies as needed
    ]
  
)