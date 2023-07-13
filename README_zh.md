<h1 align="center">
    imarkdown
</h1>
<p align="center">
  <strong>imarkdown是一个轻量级markdown图片链接转换器，你可以轻松地对图片链接进行本地到图片服务器、图片服务器到本地、图片服务器到图片服务器的转换。</strong>
</p>

[English](/README.md) [中文](/README_zh.md)

> 因为语雀转markdown的时候图片存在防外链行为，如果想要把转出的markdown发表在其他平台，就需要把markdown中所有的图片地址改成本地图片地址或者自定义的图片服务器地址，才可以让别人正常查看。该项目旨在解决这个问题，提供了一个可以批量转换markdown中的图片链接转换器，并支持一些复杂场景下的定制化转换功能。

## 功能

- 批量下载：对于markdown中的图片引用，imarkdown可以批量下载markdown中所有的图片到本地
- 多种转换方式： 对于markdown中的图片链接，支持本地转图床、web url转本地、web url转图床等多种转换方式
- 批量转换：支持单、多文件的批量转换，以及生成文件的格式化重命名等操作
- 高度自定义： 只需要继承一个MdAdapter，就可以轻松实现自定义图床的url转换
- 图床适配： 当前暂时只支持阿里云图床，欢迎pr提供更多类型图床

## 适用人群

- 有批量转换markdown图片链接url的需求的人
- 对于语雀导出markdown的用户，需要对图片外链进行转换的人
- 需要开发第三扩展应用的人

## 技术架构

`imarkdown`采用模块化设计，对于每一个组件，你都可以方便地进行扩展，下图简单展示了imarkdown的技术架构，imarkdown由以下几个部分组成：

- `MdImageConverter` Image图片转换器，负责转换markdown的图片地址并生成新的markdown文件。
- `MdAdapter` Md适配器，Image需要转换成的类型，如LocalFileAdapter本地适配器、AliyunAdapter阿里云oss适配器，CustomAdapter自定义适配器，通过将适配器注入MdImageConverter，可以定义将Image转换成什么类型的地址。
- `MdMedium` 包括MdFile和MdFolder，封装了一些特性，用于传入MdImageConverter进行数据转换。


<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230713154424.png"/>

`imarkdown`执行过程大致如下所示，在MdImageConverter执行convert方法后，imarkdown会根据传入的MdMedium构建一个虚拟MdTree，根据此树将文件进行批量图片url转换生成。

<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230713155912.png"/>

## 快速上手

该项目基于Python进行开发，使用PyPi进行发包，用户可以直接通过pip的方式轻松使用imarkdown。下面将会讲解imarkdown的几种使用场景以及使用方式。

- 第三方包安装，打开终端命令行，运行如下命令。

```sh
pip install -U imarkdown
```

**示例**
- [web url转本地地址](#web-url转本地地址)
- [web-url转图床](#web-url转图床)
- [多文件转换 web-url转本地](#多文件转换-web-url转本地)
- [多文件转换 本地转图床](#多文件转换-本地转图床)
- [自定义图床](#自定义图床)


### web url转本地地址

如果你的markdown文件里面的图片是其他网站的web url链接，而你想要将其批量下载到本地，并将markdown中的图片地址转换为本地图片地址，下面的示例将会解决你的问题。

假设你需要转换的文件为`test.md`，内容如下：

> 下面的示例如果初始markdown文件为web url，则都将基于该文档进行转换，下面不重复给出。 

```text
## 6.3 md图片地址转换
以下只支持本地传到图床

- [https://github.com/JyHu/useful_script.git](https://github.com/JyHu/useful_script.git)
- [https://github.com/JyHu/useful_script/blob/](https://github.com/JyHu/useful_script/blob/master/Scripts/md%E6%96%87%E4%BB%B6%E5%9B%BE%E7%89%87%E5%9B%BE%E5%BA%8A%E8%BD%AC%E6%8D%A2/%E8%87%AA%E5%8A%A8%E8%BD%AC%E6%8D%A2markdown%E6%96%87%E4%BB%B6%E4%B8%AD%E5%9B%BE%E7%89%87%E5%88%B0%E5%9B%BE%E5%BA%8A.md/)

罢了，折腾了这么久，又试了试这个，发现也不好用。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1670091709979-52f8c3c4-a00f-4668-a236-29ad2c09d0da.png#averageHue=%23272c34&clientId=ubb991e0d-3414-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=928&id=u4a7a8376&margin=%5Bobject%20Object%5D&name=image.png&originHeight=928&originWidth=1050&originalType=binary&ratio=1&rotation=0&showTitle=false&size=201083&status=done&style=none&taskId=u27493dc0-9d78-4c07-929c-cc946d41409&title=&width=1050)

最后，还是PigGo最香，提供了快捷键上传，上传完之后直接xxxTODO

## 6.4 Pycasbin

在pycasbin看到一个经常参与pycasbin的同行，可以参考一些他的contribution：

- [https://github.com/Nekotoxin/nekotoxin.github.io/blob/gsoc_2022_summary/GSoC2022-summary.md](https://github.com/Nekotoxin/nekotoxin.github.io/blob/gsoc_2022_summary/GSoC2022-summary.md)


![image.png](https://cdn.nlark.com/yuque/0/2022/png/26910220/1670150012015-3a93ec6b-bb27-4ed3-b42f-252a0f70b65c.png#averageHue=%23fcfbf5&clientId=u86ce0a81-ec80-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=936&id=ube9c482c&margin=%5Bobject%20Object%5D&name=image.png&originHeight=936&originWidth=1920&originalType=binary&ratio=1&rotation=0&showTitle=false&size=205691&status=done&style=none&taskId=u6a6825da-aaf4-471c-ad0e-2280c325c66&title=&width=1920)
```

该内容为本文语雀导出markdown之后的文件，其图片链接为语雀的防外链链接，需要将其图片转换到本地，并替换markdown中的链接。

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

> imarkdown中有许多需要传入路径的地方，你可以传入相对路径或者绝对路径，路径分割符推荐使用`/`而不是`\\`

转换之后的结果如下，生成一个新的markdown文件，文件名为`test_converted.md`

```text
## 6.3 md图片地址转换
以下只支持本地传到图床

- [https://github.com/JyHu/useful_script.git](https://github.com/JyHu/useful_script.git)
- [https://github.com/JyHu/useful_script/blob/](https://github.com/JyHu/useful_script/blob/master/Scripts/md%E6%96%87%E4%BB%B6%E5%9B%BE%E7%89%87%E5%9B%BE%E5%BA%8A%E8%BD%AC%E6%8D%A2/%E8%87%AA%E5%8A%A8%E8%BD%AC%E6%8D%A2markdown%E6%96%87%E4%BB%B6%E4%B8%AD%E5%9B%BE%E7%89%87%E5%88%B0%E5%9B%BE%E5%BA%8A.md/)

罢了，折腾了这么久，又试了试这个，发现也不好用。
![image.png](./images/20230713_1356451324.png)

最后，还是PigGo最香，提供了快捷键上传，上传完之后直接xxxTODO

## 6.4 Pycasbin

在pycasbin看到一个经常参与pycasbin的同行，可以参考一些他的contribution：

- [https://github.com/Nekotoxin/nekotoxin.github.io/blob/gsoc_2022_summary/GSoC2022-summary.md](https://github.com/Nekotoxin/nekotoxin.github.io/blob/gsoc_2022_summary/GSoC2022-summary.md)


![image.png](./images/20230713_1356469646.png)
```

- 自定义文件名输出
使用imarkdown进行转换，默认转换后生成的markown文件名为`{markdown_file_name}_converted.md`如果你想要自定义输出的文件名，你可以使用如下方式进行配置。

```python
md_converter.convert(md_file, name_prefix="new_", name_suffix="_converted")
```

使用该方式进行转换，最终输出的文件名为`new_test_converted.md`。如果你想要完全自定义其转换后的名字，可以使用如下方式：

```python
md_converter.convert(md_file, new_name="A new markdown.md")
```

通过上面的方式，会转换生成一个`A new markdown.md`的文件。


### web url转图床

下面的示例，我们将使用上面给出的`test.md`进行图片地址的转换，将其web url转换为阿里云oss服务器的url地址，以此展示web url转图床的功能。

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

在上面的示例中，`storage_path_prefix`表示上传到oss之后图片在bucket中的文件前缀，如你想要将图片存储在`/imarkdown`目录下，则需要设置`storage_path_prefix="/imarkdown"`。而其余的配置内容属于aliyun oss相关的配置内容，请自行填写。


### 多文件转换： web url转本地

下面的示例展示了多markdown文件批量转换，将图片web链接地址转换为本地图片地址，的解决方案。

```python
from imarkdown import LocalFileAdapter, MdFolder, MdImageConverter

def main():
    adapter = LocalFileAdapter()
    converter = MdImageConverter(adapter=adapter)
    
    # 文件名为mds
    md_folder = MdFolder(name="mds")
    # 将文件输出至converted_mds
    converter.convert(md_folder, output_directory="converted_mds")
```

使用上面的方式进行输出，将创建一个名为converted_mds的文件，转换后的文件都在保存到此，图片将保存在`converted_mds/images`中，如果你想要输出图片至指定文件，可以按照如下方式设置。

```python
md_folder = MdFolder(name="mds", image_directory="mds/my_images")
```

### 多文件转换： 本地转图床

下面的示例展示了多markdown文件批量转换，将本地图片地址转换为图床图片地址的解决方案。

```python
from imarkdown import LocalFileAdapter, MdFolder, MdImageConverter

def main():
    adapter = LocalFileAdapter()
    converter = MdImageConverter(adapter=adapter)
    
    # 文件名为local_mds，图片为本地类型，图片链接保存在"local_mds/images"
    md_folder = MdFolder(name="local_mds", image_type="local", image_directory="local_mds/images")
    # 将文件输出至converted_mds
    converter.convert(md_folder, output_directory="converted_mds")
```

### 自定义图床

下面的示例展示了如何使用imarkdown上传图片自定义的文件服务器，并获取url。

首先，你需要自定义一个适配器，并继承`BaseMdAdapter`；并实现`upload, get_replaced_url`两个方法。然后你就可以将其注入`MdImageConverter`中。

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

## 开发计划

- [ ] 添加客户端支持
- [ ] 支持腾讯云、七牛云等图床
- [x] 支持批量文件修改
- [x] 自定义适配器
- [ ] 支持大图片压缩
- [ ] 支持命令行
- [x] 支持pypi简化操作步骤
- [ ] 提供文件自定义命名
- [ ] 提供图片自定义格式化命名方式

## FAQ

**1. 如何扩展其他图床?**

如果你想开发其他图床，你唯一需要做的就是实现像`AliyunAdapter`这样的适配器，在使用的时候注入`MdImageConverter`即可，参考[自定义图床](#自定义图床)
。这就是你所需要做的。实际上，我已经把它包装好了，所以很容易扩展。

**2. 文件地址的使用**

在Python中，`/`和`\\`都可以用作文件路径的分隔符。然而，它们在使用上有一些区别。

- `/`（正斜杠）：在大多数操作系统中（包括Windows，Linux和Mac），`/`被用作文件路径的分隔符。使用`/`作为分隔符可以使代码在不同操作系统上具有可移植性。例如：

```python
path = "folder/file.txt"
```

- `\\`（反斜杠）：在Windows操作系统中，`\\`被用作文件路径的分隔符。这是因为在Windows上，`\`
  被用作转义字符，所以为了表示一个普通的反斜杠，需要使用两个连续的反斜杠。例如：

```python
path = "folder\\file.txt"
```

在使用`\\`作为分隔符时，需要注意以下几点：

- 在字符串中使用`\\`时，需要转义成`\\\\`，因为第一个`\`会被解释为转义字符。
- 可以使用原始字符串（raw string）来避免转义的麻烦。在原始字符串中，`\`不会被解释为转义字符。例如：`path = r"folder\file.txt"`

总结起来，如果你的代码需要在不同的操作系统上运行，建议使用`/`
作为文件路径的分隔符，这样可以保持代码的可移植性。如果你只在Windows上运行代码，使用`\\`也是可以的。但是，在`imarkdown`
中，所有的`\\`都会被转换为`/`。在本项目中，所有的`\\`路径最后都会被转换为`/`。

## 贡献

欢迎PRs！如果你想为这个项目做贡献，你可以提交pr或issue，[开发计划](#开发计划)中有一些可以扩展的功能，当前还有很多第三方图床需要适配，如果你在做这方面的工作，欢迎pr！我很高兴看到更多的人参与改进并优化它。
