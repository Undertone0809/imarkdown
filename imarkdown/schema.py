import glob
import os
from typing import List, Optional, Any, Dict, Union

from pydantic import BaseModel, root_validator
from typing_extensions import Literal

from imarkdown.utils import supplementary_file_path, convert_backslashes


class MdFile(BaseModel):
    name: str
    """markdown file name"""
    absolute_path: str
    """absolute path of markdown file"""
    absolute_path_name: str
    """path + name"""
    image_path: Optional[str] = None
    """image storage path if it exists"""
    image_type: Literal["local", "remote"] = "remote"
    type: Literal["original", "converted"] = "original"

    @root_validator(pre=True)
    def variables_check(cls, values: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        values["absolute_path_name"] = supplementary_file_path(values["name"])
        assert os.path.exists(
            values["absolute_path_name"]
        ), f'<{values["absolute_path_name"]}> does not exists.'
        assert (
            values["name"][-3:] == ".md"
        ), f'<{values["name"][-3:]}> is not markdown file.'

        values["absolute_path"] = "/".join(values["absolute_path_name"].split("/")[:-1])
        if "image_type" in values and values["image_type"] == "local":
            assert (
                "image_path" in values and values["image_path"]
            ), "If image_type is local, then image_path is necessary."
            values["image_path"] = supplementary_file_path(values["image_path"])
        return values


class MdFolder(BaseModel):
    name: str
    """folder name"""
    absolute_path_name: str
    sub_nodes: List[Union[MdFile, "MdFolder"]] = []
    """Current folder dir or markdown file, it contains list of MdFile and MdFolder instances."""
    image_path: Optional[str] = None
    image_type: Literal["local", "remote"] = "remote"
    type: Literal["original", "converted"] = "original"
    enable_keep_original_file_status: bool = False
    """todo not finish
    There are a pure markdown folder will be created if MdImageConverter convert MdFolder. But
    if there are some else files in the folder and you want to keep them. You can set this False."""

    @root_validator(pre=True)
    def variables_check(cls, values: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        values["absolute_path_name"] = supplementary_file_path(values["name"])
        assert os.path.exists(
            values["absolute_path_name"]
        ), f'<{values["absolute_path_name"]}> file does not exists.'
        assert os.path.isdir(
            values["absolute_path_name"]
        ), f'<{values["absolute_path_name"]}> file is not dir.'

        md_initialization_params = {"image_type": "remote", "type": "original"}

        values["name"] = values["absolute_path_name"].split("/")[-1]
        if "image_type" in values and values["image_type"] == "local":
            assert (
                "image_path" in values and values["image_path"]
            ), "If image_type is local, then image_path is necessary."
            values["image_path"] = supplementary_file_path(values["image_path"])
            md_initialization_params["image_type"] = values["image_type"]
            md_initialization_params["image_path"] = values["image_path"]

        if "type" in values and values["type"]:
            md_initialization_params["type"] = values["type"]

        # build sub nodes
        values["sub_nodes"] = []
        sub_files = glob.glob(os.path.join(values["absolute_path_name"], "*"))
        for sub_file in sub_files:
            sub_file = convert_backslashes(sub_file)
            if os.path.isdir(sub_file):
                values["sub_nodes"].append(
                    MdFolder(name=sub_file, **md_initialization_params)
                )
            if os.path.isfile(sub_file) and sub_file.endswith(".md"):
                values["sub_nodes"].append(
                    MdFile(name=sub_file, **md_initialization_params)
                )
        return values


class MdMediumManager(BaseModel):
    mediums: List[Union[MdFile, MdFolder]]
    _md_files: List[MdFile] = []

    @property
    def is_all_finished(self) -> bool:
        """Check if all md_file has completed the convert."""
        for md_file in self._md_files:
            if md_file.type == "original":
                return False
        return True

    @property
    def md_files(self) -> List[MdFile]:
        """MdFolder may contain several MdFile. This attribute will find all MdFile in mediums."""

        def find_sub_files(md_folder: MdFolder):
            for sub_node in md_folder.sub_nodes:
                if isinstance(sub_node, MdFile):
                    _cur_md_files.append(sub_node)
                elif isinstance(sub_node, MdFolder):
                    find_sub_files(sub_node)

        if self._md_files:
            return self._md_files

        _cur_md_files: List[MdFile] = []
        for medium in self.mediums:
            if isinstance(medium, MdFile):
                _cur_md_files.append(medium)
            elif isinstance(medium, MdFolder):
                find_sub_files(medium)
        return _cur_md_files
