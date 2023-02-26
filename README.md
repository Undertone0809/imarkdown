<h1 align="center">
    md-img-converter
</h1>
<p align="center">
  <strong>md-img-converter是一个markdown图片链接转换器，你可以将web链接的图片地址转换成本地地址或指定图床的地址。</strong>
</p>

[English](/README_en.md) [中文](/README.md)

> 因为语雀转markdown的时候图片存在防外链行为，如果想要把转出的markdown发表在其他平台，就需要把md中所有的图片地址改成没有放外链的地址，这样子才可以让别人正常查看。该项目旨在解决这个问题，提供了一个可以批量转换markdown中的图片链接为自己的图床的链接的转换器，并生成一个转换后的md文件。您只需要修改yaml配置就可以直接运行。

## 功能
- 批量下载markdown中所有的图片
- 上传markdown的图片到你的图床
- 替换markdown中的图片链接
- 生成一个新的markdown文件，里面的图片链接都来自`你的图床`或`本地路径文件`

## 注意事项
1. 如果你想要支持其他的图床，只自己实现一个adapter适配器即可
2. markdown中的图片链接必须是url形式的，可以从web上下载

## 快速上手

> 注意:如果你想用阿里云的图床，你的python版本必须是3.6。因为oss2最多只支持python 3.6，这个点很烦，aliyun有点懒，不维护新版本。
1. pip

```sh
pip install -r requirements.txt
```

2. config yaml
- 你需要填写`config.yaml`中的一些配置信息，下面提供了两种`config.yaml`模板，可以根据自己的需求二选一copy
- 你可以使用`test.md`来测试转换后的效果

- 如果你想要将图片link转换成阿里云图床的link
```yaml
# 需要转换的markdown文件
file_path: "test.md"
# 适配器选择，如果你想转换成你的阿里云图床
adapter: "Aliyun"
# 是否保存图片到本地
save_image: True
# Aliyun oss config
Aliyun:
  access_key_id: "your key"
  access_key_secret: "your key secret"
  bucket_name: "your bucket"
  place: "beijing"
```

- 如果你想要保存到本地

```yaml
# 需要转换的markdown文件或者包含markdown文件的目录
file_path: "test.md"
# 选择本地适配器，img路径将切换为本地路径
adapter: "Local"
```


3. 运行程序
   
- 您唯一需要做的就是运行下面的命令。

```shell script
python main.py
```

4. 生成转换后的文件

- 运行程序后，转换md图片链接后的文件名为 `yourfilename_converted.md`. 如果转换的是目录，则会以原文件名的方式保存在`<yaml_file_path>_converted_<hashcode>`文件夹下

> 如果你选择保存在本地，那么图片将保存在`images`中，在markdown中以相对路径的方式存在，因此你在移动markdown文件的时候要把对应的`images`文件一起copy走。 没有人想把它作为绝对路径，因此我并没有设置本地绝对路径的功能实现，如果你有这样的需求，欢迎pr。

## 技术框架
Actually，没有技术什么框架，但还是简单的放一个架构图吧，如果你只想要使用，则无需理会，如果你想要扩展其他图床，可以看一下。

- `Apapter` Adapter决定了Converter要将图片链接转成本地、阿里云图床还是其他图床，如果你想要开发扩展其他图床，你只需要继承一个`Apapter`类，实现`Apapter`中的三个方法，并在`ADAPTER_ENUM`中添加图床的名称即可
- `Converter` 核心部件，输入file_path和一些策略，可以利用Converter去批量修改markdown中的内容，如果你想要扩展图床，则Converter不需要修改
- `YamlConfig` config.yaml的内容用`yaml_service.py`封装了一下，用于读取一些配置信息，具体配置方法参考[快速上手](#快速上手)

<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/typora_img/20230116180115.png"/>

## 待办
- [ ] 支持更多类型的图床
- [ ] 完善单元测试
- [x] 支持批量文件修改
- [ ] 支持大图片压缩
- [ ] 支持用yaml自定义文件名、
- [ ] 支持命令行
- [ ] 支持用户界面操作
- [ ] 支持pypi简化操作步骤

## 如何扩展其他图床?
如果你想开发其他图床，你唯一需要做的就是实现像`AliyunAdapter`这样的适配器。此外，您需要配置好对应的`config.yaml`。这就是你所需要做的。实际上，我已经把它包装好了，所以很容易扩展。 


## 贡献
欢迎PRs！如果你想为这个项目做贡献，你可以提交pr或issue，[待办](#待办)中有一些可以扩展的功能。我很高兴看到更多的人参与改进并优化它。