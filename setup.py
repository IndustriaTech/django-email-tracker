from setuptools import setup, find_packages


def get_long_description():
    with open('./README.rst', 'r') as readme:
        return readme.read()

setup(
    name='django-email-tracker',
    version='0.7.1',
    description='Email Tracker for Django',
    author='Venelina Yanakieva',
    author_email='vili@magicsolutions.bg',
    maintainer='Venelin Stoykov',
    maintainer_email='venelin@magicsolutions.bg',
    url='https://github.com/IndustriaTech/django-email-tracker',
    download_url='https://github.com/IndustriaTech/django-email-tracker/releases',
    long_description=get_long_description(),
    packages=find_packages(),
    zip_safe=False,
    install_requires=['django>=1.4'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
