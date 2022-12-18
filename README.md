# md-img-converter
md-img-converter helps you convert the images address in markdown to the address of the specified graph bed.

> 因为语雀转markdown的时候图片存在防外链行为，如果想要把转出的markdown发表在其他平台，就需要把md中所有的图片地址改成没有放外链的地址，这样子才可以让别人正常查看。该项目旨在解决这个问题，提供了一个可以批量转换markdown中的图片链接为自己的图床的链接的转换器，并生成一个转换后的md文件。您只需要修改yaml配置就可以直接运行。

## Feature
- download all images of markdown
- upload image to your graph bed
- convert your markdown image in original url to your graph bed url.
- generate a new markdown by your graph bed url.

> - 批量下载markdown中所有的图片
> - 上传markdown的图片到你的图床
> - 将你原来的图片链接转换成你的图床链接
> - 生成一个新的markdown文件，里面的图片链接都来自你的图床

## Attention

1. You can write your own adapter adapter to support other graph beds
2. The link to the image in markdown must be in the form of a url and can be downloaded from the web

> 1. 读者可以自己编写一个adapter适配器，来支持其他的图床
> 2. markdown中的图片链接必须是url形式的,可以从web上下载

## Usage
> Attention: Your python version must be 3.6 if you want to use aliyun graph bed of oss2. Because oss2 only supports python 3.6 at most.

> 注意:如果你想用阿里云的图床，你的python版本必须是3.6。因为oss2最多只支持python 3.6。
1. pip

```sh
pip install -r requirements.txt
```

2. config yaml

Open `config.yaml` and config your parameters. You can test by `test.md`
```yaml
# project root markdown file name
file_path: "test.md"
# default adapter is aliyun oss
adapter: "Aliyun"
# Whether to save the image to local 
# (no image will be deleted after executing the command)
save_image: True
# Aliyun oss config
Aliyun:
  access_key_id: "your key"
  access_key_secret: "your key secret"
  bucket_name: "your bucket"
  place: "beijing"

```
3. run your Application

The only thing you need to do is just run the following command.
```shell script
python main.py
```

4. generate the converted file

New file name is `yourfilename_converted.md`.

## TODO
- [ ] support more types of graph bed.
- [ ] support command line
- [ ] support UI operate
- [ ] support pypi more easier to operate


## How to extend other graph bed?
If you want to develop other graph bed, the only thing you need to do is just implement the adapter like `AliyunApater`. Moreover, you need to config `config.yaml`.That's all you need to do. Actually, I've wrapped it so it's easy to extend. 


## Contribution
Welcome PRs! If you want to contribute to this project, you can submit pr or issue. I am glad to see more people involved and optimize it.