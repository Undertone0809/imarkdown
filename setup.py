# Copyright 2022 Zeeland(https://github.com/Undertone0809/). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pathlib

import setuptools

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="imarkdown",
    version="1.1.0",
    author="Zeeland",
    author_email="zeeland@foxmail.com",
    description="A practical Markdown image url converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Undertone0809/md-img-converter",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "pydantic==1.10.0",
        "cushy-storage"
    ],
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="Markdown, markdown, imarkdown, markdown converter",
)
