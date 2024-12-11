from setuptools import setup, find_packages

setup(
    name='anchorestig-static',
    version='0.75.0',
    description='A tool for performing static analysis using STIGs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Anchore Inc.',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'anchorestig-static=anchorestigstatic.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'click',
        'static-stig',
    ],
    python_requires='>=3.6',
)
