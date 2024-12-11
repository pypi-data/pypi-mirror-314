from setuptools import setup, find_packages
setup(
    name='quickQrLib',
    version='2.0.84',
    packages=find_packages(),
    install_requires = [
        'djangorestframework-simplejwt',
        'django',
        'djangorestframework',
        'cryptography',
        'boto3',
        'python-dateutil',
        'pytz',
        'requests',
        'redis',
        'django-environ',
        'pycryptodome',
        'prometheus_client',
    ],
    include_package_data=True,
)
