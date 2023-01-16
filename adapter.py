import oss2
import yaml_service


class Adapter:
    """
    You can implement Adapter to realize third-party 
    graph bed. For more details, you can see AliyunAdapter.
    """
    name = ''

    def upload(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def get_url(self, *args, **kwargs):
        pass


class AliyunAdapter(Adapter):
    name = 'Aliyun'

    def __init__(self):
        """ init some aliyun oss config, you should config in config.yaml """
        config = yaml_service.get_adapter_config()
        self.access_key_id = config["access_key_id"]
        self.access_key_secret = config["access_key_secret"]
        self.bucket_name = config["bucket_name"]
        self.place = config["place"]
        self.endpoint = f'http://oss-cn-{self.place}.aliyuncs.com'
        self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)

    def upload(self, key, file):
        self.bucket.put_object(key, file)

    def delete(self, key):
        self.bucket.delete_object(key)

    def get_url(self, key):
        url = f"http://{self.bucket_name}.oss-cn-{self.place}.aliyuncs.com/{key}"
        return url


class LocalAdapter(Adapter):
    name = 'Local'

    def upload(self, key, file):
        pass

    def delete(self, key):
        pass

    def get_url(self, key):
        url = f"/images/{key}"
        return url


ADAPTER_ENUM = [LocalAdapter.name, AliyunAdapter.name]
