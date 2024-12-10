from setuptools import setup, find_packages

setup(
    name='hslSixColor',
    version='0.1.4',
    author='Nayi',
    author_email='202308131171@stu.cqu.edu.cn',
    description='A package for image processing with HSL color adjustment and error diffusion dithering',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/hsl-six-color',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pillow',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
)
