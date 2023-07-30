import glob
import logging
import os
from typing import List, Optional, Any, Dict, Union

from pydantic import BaseModel, root_validator, validator
from typing_extensions import Literal

from imarkdown.utils import (
    supplementary_file_path,
    convert_backslashes,
    exist_markdown_file,
)

logger = logging.getLogger(__name__)


class BaseMdMedium(BaseModel):
    name: str
    """markdown medium name"""
    absolute_path_name: str
    """path + name"""
    image_directory: Optional[str] = None
    """image storage path if it exists"""
    image_type: Literal["local", "remote"] = "remote"
    is_default_image_directory: bool = True
    type: Literal["original", "converted"] = "original"
    output_directory: Optional[str] = None
    enable_save_images: bool = True
    enable_rename: bool = True
    root_directory: Optional[str] = None


class MdFile(BaseMdMedium):
    absolute_path: str
    """absolute path of markdown file"""

    def update_config(self, **kwargs):
        if "output_directory" in kwargs and kwargs["output_directory"]:
            self.output_directory = supplementary_file_path(kwargs["output_directory"])
            self.output_directory = self.absolute_path.replace(
                self.root_directory, self.output_directory
            )
            if self.is_default_image_directory:
                self.image_directory = f"{self.output_directory}/images"

        if "image_directory" in kwargs and kwargs["image_directory"]:
            self.image_directory = supplementary_file_path(kwargs["image_directory"])
            self.is_default_image_directory = False
        if "enable_save_images" in kwargs:
            self.enable_save_images = kwargs["enable_save_images"]
        if "enable_rename" in kwargs:
            self.enable_rename = kwargs["enable_rename"]

        os.makedirs(self.output_directory, exist_ok=True)
        os.makedirs(self.image_directory, exist_ok=True)

    @root_validator(pre=True)
    def variables_check(cls, values: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        values["absolute_path_name"] = supplementary_file_path(values["name"])
        assert os.path.exists(
            values["absolute_path_name"]
        ), f'<{values["absolute_path_name"]}> does not exists.'
        assert (
            values["name"][-3:] == ".md"
        ), f'<{values["name"][-3:]}> is not markdown file.'

        values["name"] = values["absolute_path_name"].split("/")[-1]
        values["absolute_path"] = "/".join(values["absolute_path_name"].split("/")[:-1])
        if "image_type" in values and values["image_type"] == "local":
            assert (
                "image_directory" in values and values["image_directory"]
            ), "If image_type is local, then image_directory is necessary."
            values["image_directory"] = supplementary_file_path(
                values["image_directory"]
            )
            values["is_default_image_directory"] = False
        else:
            if "image_directory" not in values or not values["image_directory"]:
                values["image_directory"] = f"{values['absolute_path']}/images"
                values["is_default_image_directory"] = True

        if "output_directory" not in values:
            values["output_directory"] = values["absolute_path"]
        os.makedirs(values["output_directory"], exist_ok=True)
        return values

    @validator("enable_save_images", always=True)
    def update_enable_save_images(
        cls, enable_save_images: bool, values: Dict[str, Any]
    ) -> bool:
        if values["image_type"] == "local" and not enable_save_images:
            raise ValueError(
                "You can not set enable_save_images = False if you original markdown file image is local url."
            )
        return enable_save_images

    @property
    def to_convert_params(self) -> Dict[str, Any]:
        params = {
            "md_file_path": self.absolute_path_name,
            "enable_rename": self.enable_rename,
            "output_md_directory": self.output_directory,
            "image_local_storage_directory": self.image_directory,
            "is_local_images": True if self.image_type == "local" else False,
            "enable_save_images": self.enable_save_images,
        }
        logger.debug(f"[imarkdown] MdFile convert params {params}")
        return params


class MdFolder(BaseMdMedium):
    sub_nodes: List[Union[MdFile, "MdFolder"]] = []
    """Current folder dir or markdown file, it contains list of MdFile and MdFolder instances."""
    is_root: bool = False
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

        md_initialization_params = {
            "image_type": "remote",
            "type": "original",
            "is_root": False,
        }

        values["name"] = values["absolute_path_name"].split("/")[-1]
        if "image_type" in values and values["image_type"] == "local":
            assert (
                "image_directory" in values and values["image_directory"]
            ), "If image_type is local, then image_directory is necessary."
            md_initialization_params["image_type"] = values["image_type"]

        if "type" in values and values["type"]:
            md_initialization_params["type"] = values["type"]

        if "output_directory" not in values:
            values["output_directory"] = values["absolute_path_name"]
        values["output_directory"] = supplementary_file_path(values["output_directory"])
        md_initialization_params["output_directory"] = values["output_directory"]
        os.makedirs(values["output_directory"], exist_ok=True)

        if "image_directory" in values and values["image_directory"]:
            values["image_directory"] = supplementary_file_path(
                values["image_directory"]
            )
        else:
            values["image_directory"] = f'{values["output_directory"]}/images'
        md_initialization_params["image_directory"] = values["image_directory"]

        if "root_directory" not in values:
            values["root_directory"] = values["output_directory"]

        if "is_root" in values and values["is_root"]:
            md_initialization_params["root_directory"] = values["output_directory"]
        else:
            md_initialization_params["root_directory"] = values["root_directory"]

        if "enable_rename" in values and values["enable_rename"]:
            md_initialization_params["enable_rename"] = values["enable_rename"]

        # build sub nodes
        values["sub_nodes"] = []
        sub_files = glob.glob(os.path.join(values["absolute_path_name"], "*"))
        for sub_file in sub_files:
            if not exist_markdown_file(sub_file):
                continue
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
    _md_files: List[MdFile] = []
    output_directory: Optional[str] = None
    enable_save_images: bool = True
    additional_kwargs: Optional[Dict[str, Any]] = None

    def update_config(
        self,
        output_directory: Optional[str] = None,
        enable_save_images: bool = True,
    ):
        """Update every md_file basic parameters."""
        if not self._md_files:
            ValueError("Please run generate_md_files firstly.")
        for md_file in self._md_files:
            params = {
                "output_directory": output_directory,
                "enable_save_images": enable_save_images,
            }
            if output_directory:
                params.update({"enable_rename": False})

            md_file.update_config(**params)

    def init_md_files(
        self,
        md_mediums: List[Union[MdFile, MdFolder]],
    ) -> List[MdFile]:
        """MdFolder may contain several MdFile.This method can convert all
        MdFolders and MdFiles to MdFiles list.

        Args:
            md_mediums(List[Union[MdFile, MdFolder]]): a list of MdFile and MdFolder

        Returns:
            A list of all MdFile.
        """
        def find_sub_files(md_folder: MdFolder):
            for sub_node in md_folder.sub_nodes:
                if isinstance(sub_node, MdFile):
                    self._md_files.append(sub_node)
                elif isinstance(sub_node, MdFolder):
                    find_sub_files(sub_node)

        for medium in md_mediums:
            if isinstance(medium, MdFile):
                self._md_files.append(medium)
            elif isinstance(medium, MdFolder):
                find_sub_files(medium)
        return self._md_files

    @property
    def md_files(self) -> List[MdFile]:
        """MdFolder may contain several MdFile. This attribute will find all MdFile in mediums."""
        if self._md_files:
            return self._md_files
        raise ValueError("Please run generate_md_files firstly.")
