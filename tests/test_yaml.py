from unittest import TestCase
import adapter
import yaml_service


class TestYaml(TestCase):

    def test_apdater_check(self):
        yaml_service.yaml_check()

    def test_adapter_type(self):
        adapter_type = yaml_service.get_adapter_type()
        ret = adapter_type in adapter.ADAPTER_ENUM
        self.assertTrue(ret)

    def test_adapater_config(self):
        adapater_config = yaml_service.get_adapter_config()
        if yaml_service.get_adapter_type() == 'Local':
            self.assertIsNone(adapater_config)
        else:
            self.assertIsNotNone(adapater_config)
