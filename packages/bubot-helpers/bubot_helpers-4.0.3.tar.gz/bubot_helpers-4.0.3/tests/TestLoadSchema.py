import unittest

from bubot_helpers.JsonSchema4 import JsonSchema4
from bubot_helpers.JsonSchemaLoader import JsonSchemaLoader


class TestLoadSchema(unittest.TestCase):
    schemas_dir = [
        'e:\\bubot4\\AdminPanel\\src\\bubot_admin_panel\\buject\\OcfSchema\\schema',
        'e:\\bubot4\\Core\\src\\bubot\\buject\\OcfSchema\\schema',
        'e:\\bubot4\\Modbus\\src\\bubot_modbus\\buject\\OcfSchema\\schema',
        'e:\\bubot4\\WebServer\\src\\bubot_webserver\\buject\\OcfSchema\\schema']

    def test_load_schema(self):
        schema = JsonSchema4()

    def test_load_bubot_schema(self):

        loader = JsonSchemaLoader(
            self.schemas_dir,
            schema_file_extension='.json'
        )
        rt = ['oic.r.openlevel']
        json_schema = JsonSchema4(loader)
        # try:
        res = json_schema.load_from_rt(rt)
        # except Exception as err:
        #     a = 1
        # pass.

    def test_load_bubot_schema2(self):
        loader = JsonSchemaLoader(
            self.schemas_dir,
            schema_file_extension='.json'
        )
        rt = ['oic.r.switch.binary']
        rt = ['bubot.serialserver.con', 'oic.wk.con', 'bubot.con']
        json_schema = JsonSchema4(loader)
        # try:
        res = json_schema.load_from_rt(rt)
        # except Exception as err:
        #     a = 1
        pass
