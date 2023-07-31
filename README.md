<h1 align="center">
    imarkdown
</h1>
<p align="center">
  <strong>imarkdown is a lightweight markdown image link converter that allows you to easily convert image links between local and image server, as well as between different image servers.</strong>
</p>

[English](/README.md) [中文](/README_zh.md)

> When converting markdown from Yuque, the images are protected against external linking. If you want to publish the converted markdown on other platforms, you need to change all the image addresses in the markdown to local image addresses or custom image server addresses, so that others can view them correctly. This project aims to solve this problem by providing a converter that can batch convert image links in markdown and supports customized conversion in complex scenarios.

## Features

- Batch Download: imarkdown can batch download all the images in the markdown that are referenced using image links.
- Multiple Conversion Methods: imarkdown supports various conversion methods for image links in markdown, such as converting to local image, converting web URL to local image, and converting web URL to image server URL.
- Batch Conversion: It supports batch conversion of single or multiple files, as well as formatting and renaming of generated files.
- Highly Customizable: By inheriting the `MdAdapter` class, you can easily implement custom URL conversion for different image servers.
- Image Server Adapters: Currently, only Aliyun OSS is supported as an image server. Contributions are welcome to add support for more types of image servers.

## Target Audience

- People who need to batch convert image links in markdown.
- Users who export markdown from Yuque and need to convert image links.
- People who need to develop third-party extensions.

## Technical Architecture

`imarkdown` is designed with a modular architecture, allowing easy extension of each component. The following diagram provides a simplified overview of the technical architecture of imarkdown, which consists of the following components:

- `MdImageConverter`: The image converter responsible for converting the image addresses in markdown and generating new markdown files.
- `MdAdapter`: The adapter for converting `Image` objects to different types, such as `LocalFileAdapter` for local conversion, `AliyunAdapter` for Aliyun OSS conversion, and `CustomAdapter` for custom conversion. By injecting the adapter into `MdImageConverter`, you can define the type of address to convert `Image` objects to.
- `MdMedium`: Includes `MdFile` and `MdFolder`, encapsulating some features used for data conversion in `MdImageConverter`.


<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230713154424.png"/>

The execution process of `imarkdown` is roughly as follows: after the `convert` method is called on `MdImageConverter`, `imarkdown` builds a virtual `MdTree` based on the provided `MdMedium`, and performs batch image URL conversion on the files according to this tree.

<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230713155912.png"/>

## Quick Start

This project is developed in Python and distributed on PyPI. Users can easily use imarkdown by installing it with pip. The following sections will explain several usage scenarios and methods of imarkdown.

- Third-Party Package Installation: Open a terminal or command prompt and run the following command.

```sh
pip install -U imarkdown
```

**Examples**
- [Convert Web URLs to Local Addresses](#converting-web-urls-to-local-file-paths)
- [Convert Web URLs to Image Server URLs](#converting-web-urls-to-image-hosting-service-urls)
- [Batch Conversion: Web URLs to Local](#batch-conversion-of-multiple-files-web-url-to-local)
- [Batch Conversion: Local to Image Server](#batch-conversion-of-multiple-files-local-to-image-hosting-service)
- [Custom Image Hosting Service](#custom-image-hosting-service)


### Converting Web URLs to Local File Paths

If you have web URL links for images in your Markdown file and you want to download them in bulk to your local machine while converting the image addresses in Markdown to local file paths, the following example will solve your problem.

Assuming the file you want to convert is `test.md` with the following content:

> The examples below will be based on the initial Markdown file if it is a web URL. They are not repeated here.

```text
## 6.3 Converting MD Image Addresses
Only supports uploading to a local image hosting service.

- [https://github.com/JyHu/useful_script.git](https://github.com/JyHu/useful_script.git)
- [https://github.com/JyHu/useful_script/blob/](https://github.com/JyHu/useful_script/blob/master/Scripts/md%E6%96%87%E4%BB%B6%E5%9B%BE%E7%89%87%E5%9B%BE%E5%BA%8A%E8%BD%AC%E6%8D%A2/%E8%87%AA%E5%8A%A8%E8%BD%AC%E6%8D%A2markdown%E6%96%87%E4%BB%B6%E4%B8%AD%E5%9B%BE%E7%89%87%E5%88%B0%E5%9B%BE%E5%BA%8A.md/)

After all the hassle and trying this, I found it doesn't work either.
![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1670091709979-52f8c3c4-a00f-4668-a236-29ad2c09d0da.png#averageHue=%23272c34&clientId=ubb991e0d-3414-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=928&id=u4a7a8376&margin=%5Bobject%20Object%5D&name=image.png&originHeight=928&originWidth=1050&originalType=binary&ratio=1&rotation=0&showTitle=false&size=201083&status=done&style=none&taskId=u27493dc0-9d78-4c07-929c-cc946d41409&title=&width=1050)

In the end, PigGo is still the best. It provides a shortcut for uploading, and after uploading, you can directly xxxTODO.

## 6.4 Pycasbin

In pycasbin, I saw a colleague who frequently contributes to pycasbin. You can refer to some of his contributions:

- [https://github.com/Nekotoxin/nekotoxin.github.io/blob/gsoc_2022_summary/GSoC2022-summary.md](https://github.com/Nekotoxin/nekotoxin.github.io/blob/gsoc_2022_summary/GSoC2022-summary.md)


![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1670150012015-3a93ec6b-bb27-4ed3-b42f-252a0f70b65c.png#averageHue=%23fcfbf5&clientId=u86ce0a81-ec80-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=936&id=ube9c482c&margin=%5Bobject%20Object%5D&name=image.png&originHeight=936&originWidth=1920&originalType=binary&ratio=1&rotation=0&showTitle=false&size=205691&status=done&style=none&taskId=u6a6825da-aaf4-471c-ad0e-2280c325c66&title=&width=1920)
```

This content is the exported Markdown file from Yuque, and its image links are protected against external access. They need to be downloaded and replaced with local file paths in the Markdown.

```python
from imarkdown import MdFile, LocalFileAdapter, MdImageConverter

def main():
    adapter = LocalFileAdapter()
    converter = MdImageConverter(adapter=adapter)
    
    md_file = MdFile(name="test.md")
    converter.convert(md_file)

if __name__ == '__main__':
    main()
```

> In imarkdown, there are many places where you need to provide paths. You can use relative paths or absolute paths. It is recommended to use `/` as the path separator instead of `\\`.

The converted result will generate a new Markdown file named `test_converted.md`, with the following content:

```text
## 6.3 Converting MD Image Addresses
Only supports uploading to a local image hosting service.

- [https://github.com/JyHu/useful_script.git](https://github.com/JyHu/useful_script.git)
- [https://github.com/JyHu/useful_script/blob/](https://github.com/JyHu/useful_script/blob/master/Scripts/md%E6%96%87%E4%BB%B6%E5%9B%BE%E7%89%87%E5%9B%BE%E5%BA%8A%E8%BD%AC%E6%8D%A2/%E8%87%AA%E5%8A%A8%E8%BD%AC%E6%8D%A2markdown%E6%96%87%E4%BB%B6%E4%B8%AD%E5%9B%BE%E7%89%87%E5%88%B0%E5%9B%BE%E5%BA%8A.md/)

After all the hassle and trying this, I found it doesn't work either.
![image.png](./images/20230713_1356451324.png)

In the end, PigGo is still the best. It provides a shortcut for uploading, and after uploading, you can directly xxxTODO.

## 6.4 Pycasbin

In pycasbin, I saw a colleague who frequently contributes to pycasbin. You can refer to some of his contributions:

- [https://github.com/Nekotoxin/nekotoxin.github.io/blob/gsoc_2022_summary/GSoC2022-summary.md](https://github.com/Nekotoxin/nekotoxin.github.io/blob/gsoc_2022_summary/GSoC2022-summary.md)


![image.png](./images/20230713_1356469646.png)
```

- Customizing the Output File Name
When using imarkdown for conversion, the default name for the converted Markdown file is `{markdown_file_name}_converted.md`. If you want to customize the output file name, you can use the following configuration:

```python
md_converter.convert(md_file, name_prefix="new_", name_suffix="_converted")
```

Using this method of conversion will result in a file named `new_test_converted.md`. If you want to completely customize the converted name, you can use the following method:

```python
md_converter.convert(md_file, new_name="A new markdown.md")
```

With the above method, a file named `A new markdown.md` will be generated.

### Converting Web URLs to Image Hosting Service URLs

In the following example, we will use the `test.md` file provided earlier to demonstrate the conversion of image addresses from web URLs to URLs on the Alibaba Cloud OSS server, showcasing the functionality of converting web URLs to image hosting service URLs.

```python
from imarkdown import MdImageConverter, AliyunAdapter, MdFile


def main():
    aliyun_config = {
        "access_key_id": "key_id",
        "access_key_secret": "key_secret",
        "bucket_name": "bucket_name",
        "place": "bucket_place",
        "storage_path_prefix": "prefix",
    }
    adapter = AliyunAdapter(**aliyun_config)
    md_converter = MdImageConverter(adapter=adapter)
    md_file = MdFile(name="markdown.md")
    md_converter.convert(md_file)


if __name__ == "__main__":
    main()
```

In the example above, `storage_path_prefix` represents the file prefix in the bucket where the image is uploaded to OSS. If you want to store the image in the `/imarkdown` directory, you need to set `storage_path_prefix="/imarkdown"`. The remaining configuration details are specific to Alibaba Cloud OSS, so please fill them in accordingly.


### Batch Conversion of Multiple Files: Web URL to Local

The following example demonstrates a solution for batch conversion of multiple Markdown files, converting web image URLs to local image addresses.

```python
from imarkdown import LocalFileAdapter, MdFolder, MdImageConverter

def main():
    adapter = LocalFileAdapter()
    converter = MdImageConverter(adapter=adapter)
    
    # Folder name is "mds"
    md_folder = MdFolder(name="mds")
    # Output files to "converted_mds"
    converter.convert(md_folder, output_directory="converted_mds")
```

Using the above code snippet will create a folder named "converted_mds" where the converted files will be saved. The images will be saved in the `converted_mds/images` directory. If you want to output the images to a specific folder, you can set it as follows:

```python
md_folder = MdFolder(name="mds", image_directory="mds/my_images")
```

### Batch Conversion of Multiple Files: Local to Image Hosting Service

The following example demonstrates a solution for batch conversion of multiple Markdown files, converting local image addresses to image hosting service URLs.

```python
from imarkdown import LocalFileAdapter, MdFolder, MdImageConverter

def main():
    adapter = LocalFileAdapter()
    converter = MdImageConverter(adapter=adapter)
    
    # Folder name is "local_mds", images are of local type, and image URLs are saved in "local_mds/images"
    md_folder = MdFolder(name="local_mds", image_type="local", image_directory="local_mds/images")
    # Output files to "converted_mds"
    converter.convert(md_folder, output_directory="converted_mds")
```

### Custom Image Hosting Service

The following example demonstrates how to use imarkdown to upload images to a custom file server and retrieve the URL.

First, you need to create a custom adapter by inheriting from `BaseMdAdapter` and implementing the `upload` and `get_replaced_url` methods. Then, you can inject the custom adapter into `MdImageConverter`.

```python
import os
import json

import requests
from imarkdown import BaseMdAdapter, MdImageConverter, MdFolder

class CustomMdAdapter(BaseMdAdapter):
    name = "custom"
    url = "https://server/upload/file/batch"
    headers = {
        "X-Upload-Token": "my_token"
    }
    cur_key = ""

    def upload(self, key: str, file):
        files = {"file": file}
        response = requests.post(self.url, headers=self.headers, files=files)
        if response.status_code == 200:
            res_data = json.loads(response.content.decode("utf-8"))
            self.cur_key = res_data["data"]["images"]["url"]
        else:
            raise Exception(response.content)

    def get_replaced_url(self, key):
        return self.cur_key

def get_all_folder_names():
    return os.listdir("my-blog")

    
def main():
    adapter = CustomMdAdapter()
    md_converter = MdImageConverter(adapter=adapter)

    md_folders = []
    for folder_name in get_all_folder_names():
        md_folders.append(
            MdFolder(
                name=f"my-blog/{folder_name}",
                image_directory=f"my-blog/{folder_name}/images",
                image_type="local",
            )
        )
    md_converter.convert(md_folders, output_directory="converted")


if __name__ == "__main__":
    main()
```

### Custom Regular Expression
`imarkdown` use regular expression to find your images. It supports `![](image_url)` and `<img src="image_url"/>` format, but there are still some other format `imarkdown` can not find it.

At this point, `imarkdown` supports custom regular expression to address this issue. You can customize a regular expression which can find your markdown image url and pass it to MdImageConverter. The following example show how to use it.

```python
from imarkdown import MdImageConverter, LocalFileAdapter, MdFolder


def main():
    custom_re = r"(?:!\[(.*?)\]\((.*?)\))|<img.*?src=[\'\"](.*?)[\'\"].*?>"
    adapter = LocalFileAdapter()
    md_converter = MdImageConverter(adapter=adapter)
    
    md_folder = MdFolder(name="mds")
    md_converter.convert(md_folder, output_directory="output_mds", re_rule=custom_re)


if __name__ == "__main__":
    main()
```

## Roadmap

- [ ] Add client-side support
- [ ] Support Tencent Cloud, Qiniu Cloud, and other image hosting services
- [x] Support batch file modification
- [x] Custom adapters
- [ ] Support compression of large images
- [ ] Support command-line interface
- [x] Support PyPI for simplified operations
- [ ] Provide file custom naming
- [ ] Provide custom formatting for image names

## FAQ

**1. How can I extend to other image hosting services?**

If you want to develop support for other image hosting services, all you need to do is implement an adapter similar to `AliyunAdapter` and inject it into `MdImageConverter` when using it. Refer to [Custom Image Hosting Service](#custom-image-hosting-service). That's all you need to do. In fact, I've wrapped it up nicely, so extending it is straightforward.

**2. Usage of file addresses**

In Python, both `/` and `\\` can be used as file path separators. However, there are some differences in their usage.

- `/` (forward slash): In most operating systems, including Windows, Linux, and Mac, `/` is used as the file path separator. Using `/` as the separator can make your code portable across different operating systems. For example:

```python
path = "folder/file.txt"
```

- `\\` (backslash): In the Windows operating system, `\\` is used as the file path separator. This is because `\` is used as an escape character in Windows, so to represent a plain backslash, you need to use two consecutive backslashes. For example:

```python
path = "folder\\file.txt"
```

When using `\\` as the separator, keep the following points in mind:

- When using `\\` in a string, you need to escape it as `\\\\` because the first `\` will be interpreted as an escape character.
- You can use raw strings to avoid the hassle of escaping. In a raw string, `\` is not interpreted as an escape character. For example: `path = r"folder\file.txt"`

In summary, if your code needs to run on different operating systems, it is recommended to use `/` as the file path separator to maintain code portability. If you are only running the code on Windows, using `\\` is also acceptable. However, in `imarkdown`, all `\\` paths will be converted to `/`. In this project, all `\\` paths will be converted to `/`.

## Contribution

Contributions are welcome! If you would like to contribute to this project, you can submit a pull request or an issue. There are some extensible features listed in the [Development Roadmap](#development-roadmap), and there are still many third-party image hosting services that need to be adapted. If you are working on these aspects, feel free to submit a pull request! I'm excited to see more people involved in improving and optimizing it.