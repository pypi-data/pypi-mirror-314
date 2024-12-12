from setuptools import setup, find_packages

setup(
    name='WinKeyBoard',
    version='0.1.2',
    author='AWang_Dog',
    author_email='AWangDog@126.com',
    description='Windows下的键盘控制',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AWangDog/WinKeyBoard',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.9',
)
