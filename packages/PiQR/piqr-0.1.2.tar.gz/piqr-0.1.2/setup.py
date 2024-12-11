from setuptools import setup, find_packages

setup(
    name='PiQR',
    version='0.1.2',
    author='PimpDiCaprio',
    author_email='info@aperturesoftware.us',
    description='A Python library for displaying QR codes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PimpDiCaprio/PiQR',
    packages=find_packages(),
    scripts=['PiQR.py'],
    install_requires=[
        'opencv-contrib-python',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)