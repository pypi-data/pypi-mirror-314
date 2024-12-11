from setuptools import setup, find_packages

setup(
    name='zaz_aangaraa_pay_python',
    version='0.1.0',
    description='A Python package for integrating MTN and Orange Money payments in Cameroon',
    author='Achaire Zogo',
    author_email='dylanabouma@gmail.com',
    url='https://github.com/Achaire-Zogo/aangaraa_pay_python',
    packages=find_packages(),
    install_requires=[
        'requests',  # For making HTTP requests
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
