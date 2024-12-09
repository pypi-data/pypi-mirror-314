from setuptools import setup

setup(
    name='ue5-tools',
    version='0.1.0',
    packages=['ue5'],
    url='https://github.com/retroandchill/ue5-tools',
    author='Retro & Chill',
    description='UE5 Python helper tools',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'conan>=2.9.2'
    ],
)