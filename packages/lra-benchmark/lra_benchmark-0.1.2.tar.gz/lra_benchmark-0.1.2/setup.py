from setuptools import setup, find_packages

setup(
    name="lra_benchmark",
    version="0.1.2",
    author="Sami Agourram",
    author_email="agourram.ma@gmail.com",
    description="A library for benchmarking lightweight Vision Transformers following the LRA methodology",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SamiAGOURRAM/LRA-Benchmark-for-image-classification-on-CIFAR-10.git",
    packages=find_packages(),
    install_requires=[
        "torch",
        "torchvision",
        "timm",
        "pytorch-lightning"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires=">=3.7",
)
