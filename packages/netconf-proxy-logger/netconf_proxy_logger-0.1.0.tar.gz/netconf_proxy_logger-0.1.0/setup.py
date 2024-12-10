from setuptools import setup, find_packages

setup(
    name='netconf-proxy-logger',
    version='0.1.0',
    author='Satyajit Ghosh',
    author_email='contact@satyajit.co.in',
    description='A NETCONF proxy server with comprehensive logging capabilities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SATYAJIT1910/netconf-proxy-logger',
    packages=find_packages(),
    install_requires=[
        'paramiko>=3.1.0,<4.0.0',  
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
        'Topic :: System :: Networking',
    ],
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'netconflog=netconf_proxy_logger.handler:main',
        ],
    },
    keywords='netconf proxy logging network automation',
)