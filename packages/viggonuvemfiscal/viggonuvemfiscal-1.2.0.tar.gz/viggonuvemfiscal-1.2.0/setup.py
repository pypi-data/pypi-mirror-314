from setuptools import setup, find_packages

REQUIRED_PACKAGES = [
    'viggocore>=1.0.0,<2.0.0',
    'flask-cors'
]

setup(
    name="viggonuvemfiscal",
    version="1.2.0",
    summary='ViggoNuvemFiscal Module Framework',
    description="ViggoNuvemFiscal backend Flask REST service",
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED_PACKAGES
)
