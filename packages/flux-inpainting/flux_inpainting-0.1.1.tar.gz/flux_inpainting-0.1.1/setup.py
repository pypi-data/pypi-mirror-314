from setuptools import setup, find_packages

setup(
    name='flux_inpainting',  # Name of your package
    version='0.1.1',   # Version of your package
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=['diffusers','torch','transformers','accelerate','huggingface_hub','sentencepiece'],  # List any dependencies your package has here
    author='Amit Kumar',
    author_email='amit.ceg.official@gmail.com',
    description='A simple example package',
    #long_description=open('README.md').read(),  # Optional, long description from README
    long_description_content_type='text/markdown',
    url='https://github.com/geekforai/flux_inpainting',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
