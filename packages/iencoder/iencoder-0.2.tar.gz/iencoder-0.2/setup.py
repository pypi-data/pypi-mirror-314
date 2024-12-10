from setuptools import setup, find_packages

setup(
    name='iencoder',  
    version='0.2',  
    packages=find_packages(),  
    description='Custom encoder for handling categorical variables with special encoding techniques.',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    author='Anida Nezovic',  
    author_email='nezovicanida@gmail.com', 
    url='https://github.com/anezovic1/i-encoding',  
    license='MIT',  
    classifiers=[  
        'Development Status :: 3 - Alpha',  
        'Intended Audience :: Science/Research',  
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',  
    install_requires=[  
        'numpy',  
        'pandas',
        'scikit-learn',
    ],
    include_package_data=True,  
)
