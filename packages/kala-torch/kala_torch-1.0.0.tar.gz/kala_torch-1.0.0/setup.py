from setuptools import setup, find_packages

setup(
    name='kala_torch',
    version='1.0.0',
    description='A PyTorch-based module for easy implementation of various AI models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='N V R K Sai Kamesh Sharma',
    author_email='your-email@example.com',
    url='https://github.com/yourusername/kala_torch',  # Replace with your GitHub URL
    packages=find_packages(),
    install_requires=[
        'torch>=1.0',
        'torchvision>=0.3.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
