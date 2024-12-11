#!/usr/bin/env python3
"""
Base formatter for SPM data.
"""

# -*- coding: utf-8 -*-
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
from abc import ABC, abstractmethod
from typing import Dict, Union, List, Optional, TYPE_CHECKING
from dataclasses import dataclass
from pynxtools_spm.parsers import SPMParser
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.readers.utils import FlattenSettings, flatten_and_replace
import yaml
from pynxtools_spm.nxformatters.helpers import (
    _get_data_unit_and_others,
    to_intended_t,
    replace_variadic_name_part,
)
from pathlib import Path
import numpy as np

from pynxtools_spm.nxformatters.helpers import replace_variadic_name_part


if TYPE_CHECKING:
    from pint import Quantity


REPLACE_NESTED: Dict[str, str] = {}

CONVERT_DICT = {
    "Positioner_spm": "POSITIONER_SPM[positioner_spm]",
    "Temperature": "TEMPERATURE[temperature]",
    "Scan_control": "SCAN_CONTROL[scan_control]",
    "unit": "@units",
    "version": "@version",
    "default": "@default",
    "Sample": "SAMPLE[sample]",
    "History": "HISTORY[history]",
    "User": "USER[user]",
    "Data": "DATA[data]",
    "Source": "SOURCE[source]",
    "Mesh_scan": "mesh_SCAN[mesh_scan]",
}

PINT_QUANTITY_MAPPING = {
    "[mass] * [length] ** 2 / [time] ** 3 / [current]": "voltage",
    "[mass] * [length] ** 2 / [current] / [time] ** 3": "voltage",
    "[length] ** 2 * [mass] / [time] ** 3 / [current]": "voltage",
    "[length] ** 2 * [mass] / [current] / [time] ** 3": "voltage",
    "[current]": "current",
}


@dataclass
class NXdata:
    grp_name: Optional[str] = ""
    signal: Optional[str] = None
    auxiliary_signals: Optional[List[str]] = None
    title: Optional[str] = None


class SPMformatter(ABC):
    # Map function to deal specific group. Map key should be the same as it is
    # in config file
    _grp_to_func: dict[str, str] = {}  # Placeholder
    _axes: list[str] = []  # Placeholder

    # Class used to colleted data from several subgroups of ScanControl and reuse them
    # in the subgroups
    @dataclass
    class NXScanControl:  # TODO: Rename this class NXimageScanControl and create another class for BiasSpectroscopy
        # Put the class in the base_formatter.py under BaseFormatter class
        x_points: int
        y_points: int
        x_start: Union[int, float]
        x_start_unit: Union[str, "Quantity"]
        y_start: Union[int, float]
        y_start_unit: Union[str, "Quantity"]
        x_range: Union[int, float]
        y_range: Union[int, float]
        x_end: Union[int, float]
        x_end_unit: Union[str, "Quantity"]
        y_end: Union[int, float]
        y_end_unit: Union[str, "Quantity"]
        fast_axis: str  # lower case x, y
        slow_axis: str  # lower case x, y

    def __init__(
        self,
        template: Template,
        raw_file: Union[str, "Path"],
        eln_file: str | Path,
        config_file: str | Path | None = None,  # Incase it is not provided by users
        entry: Optional[str] = None,
    ):
        self.template: Template = template
        self.raw_file: Union[str, "Path"] = raw_file
        self.eln = self._get_eln_dict(eln_file)  # Placeholder
        self.raw_data: Dict = self.get_raw_data_dict()
        self.entry: str = entry
        self.config_dict = self._get_conf_dict(config_file) or None  # Placeholder

    @abstractmethod
    def _get_conf_dict(self, config_file: str | Path = None): ...

    def _get_eln_dict(self, eln_file: str | Path):
        with open(eln_file, mode="r", encoding="utf-8") as fl_obj:
            eln_dict = flatten_and_replace(
                FlattenSettings(yaml.safe_load(fl_obj), CONVERT_DICT, REPLACE_NESTED)
            )
        return eln_dict

    def walk_though_config_nested_dict(
        self, config_dict: Dict, parent_path: str, use_custom_func_prior: bool = True
    ):
        # This concept is just note where the group will be
        # handeld or somthing like that.
        if "#note" in config_dict:
            return
        for key, val in config_dict.items():
            if val is None or val == "":
                continue
            # Special case, will be handled in a specific function registerd
            # in self._grp_to_func
            if key in self._grp_to_func:
                if not use_custom_func_prior:
                    self.walk_though_config_nested_dict(
                        config_dict=val, parent_path=f"{parent_path}/{key}"
                    )
                    # Fill special fields first
                    method = getattr(self, self._grp_to_func[key])
                    method(val, parent_path, key)
                else:
                    method = getattr(self, self._grp_to_func[key])
                    method(val, parent_path, key)
                    self.walk_though_config_nested_dict(
                        config_dict=val, parent_path=f"{parent_path}/{key}"
                    )

            # end dict of the definition path that has raw_path key
            elif isinstance(val, dict) and "raw_path" in val:
                if "#note" in val:
                    continue
                data, unit, other_attrs = _get_data_unit_and_others(
                    data_dict=self.raw_data, end_dict=val
                )
                self.template[f"{parent_path}/{key}"] = to_intended_t(data)
                self.template[f"{parent_path}/{key}/@units"] = unit
                if other_attrs:
                    for k, v in other_attrs.items():
                        self.template[f"{parent_path}/{key}/@{k}"] = v
            # Handle to construct nxdata group that comes alon as a dict
            elif (
                isinstance(val, dict)
                and ("@title" in val or "grp_name" in val)
                and "data" in val
            ):
                _ = self._NXdata_grp_from_conf_description(
                    partial_conf_dict=val,
                    parent_path=parent_path,
                    group_name=key,
                )
            # variadic fields that would have several values according to the dimentions
            elif isinstance(val, list) and isinstance(val[0], dict):
                for item in val:
                    # Handle to construct nxdata group
                    if (
                        isinstance(item, dict)
                        and ("@title" in item or "grp_name" in item)
                        and "data" in item
                    ):
                        _ = self._NXdata_grp_from_conf_description(
                            partial_conf_dict=item,
                            parent_path=parent_path,
                            group_name=key,
                        )
                    else:  # Handle fields and attributes
                        part_to_embed, path_dict = (
                            item.popitem()
                        )  # Current only one item is valid
                        # with #note tag this will be handled in a specific function
                        if "#note" in path_dict:
                            continue
                        data, unit, other_attrs = _get_data_unit_and_others(
                            data_dict=self.raw_data, end_dict=path_dict
                        )
                        temp_key = f"{parent_path}/{replace_variadic_name_part(key, part_to_embed=part_to_embed)}"
                        self.template[temp_key] = to_intended_t(data)
                        self.template[f"{temp_key}/@units"] = unit
                        if other_attrs:
                            for k, v in other_attrs.items():
                                self.template[f"{temp_key}/@{k}"] = v

            else:
                self.walk_though_config_nested_dict(val, f"{parent_path}/{key}")

    def rearrange_data_according_to_axes(self, data, is_forward: Optional[bool] = None):
        """Rearrange array data according to the fast and slow axes.

        Parameters
        ----------
        data : np.ndarray
            Two dimensional array data from scan.
        is_forward : bool, optional
            Default scan direction.
        """

        # if NXcontrol is not defined (e.g. for Bias Spectroscopy)
        if not hasattr(self.NXScanControl, "fast_axis") and not hasattr(
            self.NXScanControl, "slow_axis"
        ):
            return data
        fast_axis, slow_axis = (
            self.NXScanControl.fast_axis,
            self.NXScanControl.slow_axis,
        )

        # TODO recheck the logic
        # Coodinate of the data points exactly the same as the scan region
        # is defined. E.g if the scan starts from the top left corner then
        # that is the origin of the plot. In plot visualization the origin
        # starts botoom left conrner.

        rearraged = None
        if fast_axis == "x":
            if slow_axis == "-y":
                rearraged = np.flipud(data)
            rearraged = data
        elif fast_axis == "-x":
            if slow_axis == "y":
                rearraged = np.fliplr(data)
            elif slow_axis == "-y":
                # np.flip(data)
                np.flip(data)
        elif fast_axis == "-y":
            rearraged = np.flipud(data)
            if slow_axis == "-x":
                rearraged = np.fliplr(rearraged)
        elif fast_axis == "y":
            rearraged = data
            if slow_axis == "-x":
                rearraged = np.fliplr(rearraged)
        else:
            rearraged = data
        # Consider backward scan
        if is_forward is False:
            rearraged = np.fliplr(rearraged)
        return rearraged

    def get_raw_data_dict(self):
        return SPMParser().get_raw_data_dict(self.raw_file, eln=self.eln)

    def _arange_axes(self, direction="down"):
        fast_slow: List[str]
        if direction.lower() == "down":
            fast_slow = ["-Y", "X"]
        elif direction.lower() == "up":
            fast_slow = ["Y", "X"]
        elif direction.lower() == "right":
            fast_slow = ["X", "Y"]
        elif direction.lower() == "left":
            fast_slow = ["-X", "Y"]
        else:
            fast_slow = ["X", "Y"]
        self.NXScanControl.fast_axis = fast_slow[0].lower()
        self.NXScanControl.slow_axis = fast_slow[1].lower()

        return fast_slow

    @abstractmethod
    def get_nxformatted_template(self): ...

    def _format_template_from_eln(self):
        for key, val in self.eln.items():
            self.template[key] = to_intended_t(val)

    @abstractmethod
    def _construct_nxscan_controllers(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name: str,
        *arg,
        **kwarg,
    ): ...

    # TODO: Try to use decorator to ge the group name at some later stage
    def _NXdata_grp_from_conf_description(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name: str,
        group_index=0,
        is_forward: Optional[bool] = None,
    ):
        """Example NXdata dict descrioption from config
        partial_conf_dict = {
            "data": {
                "name": "temperature1(filter)",
                "raw_path": "/dat_mat_components/Temperature 1 [filt]/value",
                "@units": "/dat_mat_components/Temperature 1 [filt]/unit",
            },
            "0": {
                "name": "Bias Voltage",
                "raw_path": [
                    "/dat_mat_components/Bias calc/value",
                    "/dat_mat_components/Bias/value",
                ],
                "@units": [
                    "/dat_mat_components/Bias calc/unit",
                    "/dat_mat_components/Bias/unit",
                ],
                "axis_ind": 0,
            },
            "@title": "Bias Spectroscopy Temperature1(filter)",
            "grp_name": "temperature1(filter)",
        }
        To get the proper relation please visit:

        args:
        -----
            "data" -> Signal data of "temperature1(filter)" denoted by
                    the name key.
            "0" -> Index of the axis if "axis_ind" is not provided.
                    Here both are same. Name of the axis is denoted
                    by the name key.
            "title" -> Title of the main plot.
            "grp_name" -> Name of the NXdata group.
            is_forward -> Direction of the scan. Default is True.

        return:
        -------
            str: Name of the NXdata group.

        """
        grp_name_to_embed = partial_conf_dict.get("grp_name", f"data_{group_index}")
        if "grp_name" in partial_conf_dict:
            del partial_conf_dict["grp_name"]

        grp_name_to_embed_fit = grp_name_to_embed.replace(" ", "_").lower()
        nxdata_group = replace_variadic_name_part(group_name, grp_name_to_embed_fit)
        data_dict = partial_conf_dict.get("data")
        nxdata_nm = data_dict.pop("name", "")
        nxdata_d_arr, d_unit, d_others = _get_data_unit_and_others(
            self.raw_data, end_dict=data_dict
        )
        if not isinstance(nxdata_d_arr, np.ndarray):
            return
        # nxdata_title = partial_conf_dict.get("title", "title")
        nxdata_axes = []
        nxdata_indices = []
        axdata_unit_other_list = []
        # Handle axes
        for key, val in partial_conf_dict.items():
            if key == "data":  # handled above
                continue
            if isinstance(val, dict):
                try:
                    index = int(key)
                except ValueError:
                    continue
                nxdata_axes.append(val.pop("name", ""))
                index = val.pop("axis_ind", index)
                nxdata_indices.append(index)
                axdata_unit_other_list.append(
                    _get_data_unit_and_others(self.raw_data, end_dict=val)
                )
        field_nm_fit = nxdata_nm.replace(" ", "_").lower()
        self.template[f"{parent_path}/{nxdata_group}/@title"] = (
            f"Title Data Group {group_index}"
        )
        self.template[f"{parent_path}/{nxdata_group}/{field_nm_fit}"] = (
            self.rearrange_data_according_to_axes(nxdata_d_arr, is_forward=is_forward)
        )
        self.template[f"{parent_path}/{nxdata_group}/{field_nm_fit}/@units"] = d_unit
        self.template[f"{parent_path}/{nxdata_group}/{field_nm_fit}/@long_name"] = (
            f"{nxdata_nm} ({d_unit})"
        )
        self.template[f"{parent_path}/{nxdata_group}/@signal"] = field_nm_fit
        if d_others:
            for k, v in d_others.items():
                k = k.replace(" ", "_").lower()
                # TODO check if k starts with @ or not
                k = k[1:] if k.startswith("@") else k
                self.template[f"{parent_path}/{nxdata_group}/{field_nm_fit}/@{k}"] = v
        if not (len(nxdata_axes) == len(nxdata_indices) == len(axdata_unit_other_list)):
            return

        for ind, (index, axis) in enumerate(zip(nxdata_indices, nxdata_axes)):
            axis_fit = axis.replace(" ", "_").lower()
            self.template[f"{parent_path}/{nxdata_group}/@{axis_fit}_indices"] = index
            self.template[f"{parent_path}/{nxdata_group}/{axis_fit}"] = (
                axdata_unit_other_list[ind][0]
            )
            unit = axdata_unit_other_list[ind][1]
            self.template[f"{parent_path}/{nxdata_group}/{axis_fit}/@units"] = unit
            self.template[f"{parent_path}/{nxdata_group}/{axis_fit}/@long_name"] = (
                f"{axis} ({unit})"
            )
            if axdata_unit_other_list[ind][2]:  # Other attributes
                for k, v in axdata_unit_other_list[ind][2].items():
                    self.template[f"{parent_path}/{nxdata_group}/{axis_fit}/{k}"] = v

        self.template[f"{parent_path}/{nxdata_group}/@axes"] = [
            ax.replace(" ", "_").lower() for ax in nxdata_axes
        ]
        # Read grp attributes from config file
        for key, val in partial_conf_dict.items():
            if key in ("grp_name",) or isinstance(val, dict) or key.startswith("#"):
                continue
            elif key.startswith("@"):
                self.template[f"{parent_path}/{nxdata_group}/{key}"] = val

        return nxdata_group
