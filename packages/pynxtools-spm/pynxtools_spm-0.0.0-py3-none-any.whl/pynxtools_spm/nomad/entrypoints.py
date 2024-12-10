#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
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
#
"""Entry points for STS and STM examples."""

from nomad.config.models.plugins import ExampleUploadEntryPoint

sts_default_example = ExampleUploadEntryPoint(
    title="Scanning Tunneling Spectroscopy (STS)",
    category="SPM experiments examples (with default configuration)",
    description="""This example (with default configuration) presents the capabilities of the NOMAD platform to store standardized Scanning Tunneling Spectroscopy (sts) data.""",
    plugin_package="pynxtools_spm",
    resources=["nomad/examples/sts/STSDefaultExample/*"],
)
sts_example_with_customization = ExampleUploadEntryPoint(
    title="Scanning Tunneling Spectroscopy (STS)",
    category="SPM experiments examples (with customization options)",
    description="""This example (with customization options) presents the capabilities of the NOMAD platform to store standardized Scanning Tunneling Spectroscopy (sts) data""",
    plugin_package="pynxtools_spm",
    resources=["nomad/examples/sts/STSExampleWithCustomization/*"],
)

stm_default_example = ExampleUploadEntryPoint(
    title="Scanning Tunneling Microscopy (STM)",
    category="SPM experiments examples (with default configuration)",
    description="""This example (with default configuration) presents the capabilities of the NOMAD platform to store standardized Scanning Tunneling Microscopy (stm) data.""",
    plugin_package="pynxtools_spm",
    resources=["nomad/examples/stm/STMDefaultExample/*"],
)
stm_example_with_customization = ExampleUploadEntryPoint(
    title="Scanning Tunneling Microscopy (STM)",
    category="SPM experiments examples (with customization options)",
    description="""This example (with customization options) presents the capabilities of the NOMAD platform to store standardized Scanning Tunneling Microscopy (stm) data""",
    plugin_package="pynxtools_spm",
    resources=["nomad/examples/stm/STMExampleWithCustomization/*"],
)

afm_default_example = ExampleUploadEntryPoint(
    title="Atomic Force Microscopy (AFM)",
    category="SPM experiments examples (with default configuration)",
    description="""This example (with default configuration) presents the capabilities of the NOMAD platform to store standardized Atomic Force Microscopy (afm) data.""",
    plugin_package="pynxtools_spm",
    resources=["nomad/examples/afm/AFMDefaultExample/*"],
)
afm_example_with_customization = ExampleUploadEntryPoint(
    title="Atomic Force Microscopy (AFM)",
    category="SPM experiments examples (with customization options)",
    description="""This example (with customization options) presents the capabilities of the NOMAD platform to store standardized Atomic Force Microscopy (afm) data""",
    plugin_package="pynxtools_spm",
    resources=["nomad/examples/afm/AFMExampleWithCustomization/*"],
)
