from setuptools import setup, find_packages

setup(
    name='vidcov',
    version='1.0.0',
    description='A script for setting a thumbnail on a video file using ffmpeg',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Avinion',
    author_email='shizofrin@gmail.com',
    url='https://x.com/Lanaev0li',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'vidcov = vidcov.vidcov:set_video_thumbnail',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)