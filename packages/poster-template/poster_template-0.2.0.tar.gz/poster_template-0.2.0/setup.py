from setuptools import setup, find_packages

setup(
    name='poster_template',  # Name of your package
    version='0.2.0',   # Version of your package
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=['pillow','numpy'],  # List any dependencies your package has here
    author='Amit Kumar',
    author_email='amit.ceg.official@gmail.com',
    description='A simple example package',
    #long_description=open('README.md').read(),  # Optional, long description from README
    long_description_content_type='text/markdown',
    url='https://github.com/geekforai/poster_template',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
