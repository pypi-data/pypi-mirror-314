#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="sentry-plugin-ph",
    version='0.0.5',
    author='ding',
    description='ph notification plugin for Sentry',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'sentry>=9.0.0',
        'markdown>=3.0.0',
    ],
    entry_points={
        'sentry.plugins': [
            'dingtalk = sentry_plugin_dingtalk.plugin:DingtalkPlugin'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
