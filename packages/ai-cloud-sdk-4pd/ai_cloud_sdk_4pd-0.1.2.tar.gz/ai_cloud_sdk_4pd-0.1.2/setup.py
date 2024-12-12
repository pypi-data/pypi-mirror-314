import os

from setuptools import setup, find_packages

PACKAGE = 'ai_cloud_sdk_4pd'
NAME = 'ai_cloud_sdk_4pd'
DESCRIPTION = '4paradigm AI Cloud Service SDK Library for Python'
AUTHOR = '4paradigm AI Cloud SDK'
AUTHOR_EMAIL = ''
URL = 'https://gitlab.4pd.io/ai_clound_platform/4pd-ai-clound-sdk'
VERSION = '0.1.2'
REQUIRES = [
    'requests',
    'websockets==10.4',
]

LONG_DESCRIPTION = ''
if os.path.exists('./README.md'):
    with open('README.md', encoding='utf-8') as fp:
        LONG_DESCRIPTION = fp.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    # license='Apache License 2.0',
    url=URL,
    keywords=['4pd_ai_cloud'],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    platforms='any',
    install_requires=REQUIRES,
    python_requires='>=3.6',
    classifiers=[
        # 'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
    ],
)
