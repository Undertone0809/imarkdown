<h1 align="center">
    md-img-converter
</h1>
<p align="center">
  <strong>md-img-converter helps you convert the images address in markdown to the address of the specified graph bed.</strong>
</p>

[English](/README_en.md) [中文](/README.md)

## Feature
- download all images of markdown
- upload image to your graph bed
- convert your markdown image in original url to your graph bed url.
- generate a new markdown by your graph bed url.


## Attention

1. You can write your own adapter adapter to support other graph beds
2. The link to the image in markdown must be in the form of a url and can be downloaded from the web


## Usage
> Attention: Your python version must be 3.6 if you want to use aliyun graph bed of oss2. Because oss2 only supports python 3.6 at most.

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
If you want to develop other graph bed, the only thing you need to do is just implement the adapter like `AliyunAdapter`. Moreover, you need to config `config.yaml`.That's all you need to do. Actually, I've wrapped it so it's easy to extend. 


## Contribution
Welcome PRs! If you want to contribute to this project, you can submit pr or issue. I am glad to see more people involved and optimize it.