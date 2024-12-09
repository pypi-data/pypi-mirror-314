import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "affinidi_tdk_iota_core",
    "version": "1.21.0",
    "description": "Affinidi Iota Framework core library primarily used in the backend",
    "license": "Apache-2.0",
    "url": "https://github.com/affinidi/affinidi-tdk#readme",
    "long_description_content_type": "text/markdown",
    "author": "Affinidi",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/affinidi/affinidi-tdk"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "affinidi_tdk_iota_core",
        "affinidi_tdk_iota_core._jsii"
    ],
    "package_data": {
        "affinidi_tdk_iota_core._jsii": [
            "iota-core@1.21.0.jsii.tgz"
        ],
        "affinidi_tdk_iota_core": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "jsii>=1.105.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
