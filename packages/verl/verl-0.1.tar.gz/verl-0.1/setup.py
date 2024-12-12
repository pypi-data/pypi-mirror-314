# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages
import os

version_folder = os.path.dirname(os.path.join(os.path.abspath(__file__)))

with open(os.path.join(version_folder, 'verl/version/version')) as f:
    __version__ = f.read().strip()

# TODO: add version info to requirements
install_requires = [
    'torch==2.4.0',
    'tensordict',
    'transformers',
    'codetiming',
    'pybind11',
    'hydra-core',
    'numpy',
    'yapf',
    "dill",
    "accelerate"
]

install_optional = [
    'vllm==0.6.3',
]

extras_require = {
    'demo': ['hydra-core', 'transformers', ''],
    'single-controller': ['ray', 'kubernetes'],
    'single-controller-ray': ['ray'],
    'test': ['fsspec', 'pytest', 'datasets']
}

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='verl',
    version=__version__,
    package_dir={'': '.'},
    packages=find_packages(where='.'),
    url='https://github.com/volcengine/verl',
    license='Apache 2.0',
    author='Bytedance - Seed - MLSys',
    author_email='zhangchi.usc1992@bytedance.com, gmsheng@connect.hku.hk',
    description='veRL: Volcano Engine Reinforcement Learning for LLM',
    install_requires=install_requires,
    extras_require=extras_require,
    package_data={'': ['version/*'],
                  'verl': ['trainer/config/*.yaml'],},
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
