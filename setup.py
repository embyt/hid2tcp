"""setup module for hid2tcp"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# needed packages
REQUIRES = [
    'pyusb',
    'pep3143daemon',
]

setup(
    name='hid2tcp',
    version='0.1.0',
    description='hid2tcp provides access to USB HID device via a TCP port. To access the USB device it uses libusb.',
    url='https://github.com/romor/hid2tcp',
    author='Roman Morawek',
    author_email='maemo@morawek.at',
    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='usb hid tcp port python',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=REQUIRES,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'hid2tcp=hid2tcp.hid2tcp:main',
        ],
    },
)
