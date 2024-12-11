from setuptools import setup, find_namespace_packages


setup(
    name='brynq_sdk_sodeco',
    version='0.0.4',
    description='Sodeco wrapper from BrynQ',
    long_description='Sodeco wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=find_namespace_packages(include=['brynq_sdk.*']),
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'brynq-sdk-functions>=1',
        'pandera>=0.18.0'
    ],
    zip_safe=False,
)