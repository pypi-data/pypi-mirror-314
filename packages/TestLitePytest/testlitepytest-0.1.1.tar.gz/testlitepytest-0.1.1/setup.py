from setuptools import setup, find_packages

setup(
    name='TestLitePytest',  # Replace with your package’s name
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests>=2.32.3',
        'pytest>=8.3.2'
    ],
    author='Dmitry Skryabin',  
    author_email='skryabind98@gmail.com',
    description='Pytest adaptor for TestLite TMS system',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',

)