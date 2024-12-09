import unittest
from Bubot.Helpers.Helper import Helper


class TestUpdateDict(unittest.TestCase):
    def test_update_string_array(self):
        a = {'t': ['a1', 'a2', 'a3']}
        b = {'t': ['a1', 'a4', 'a3']}
        res = Helper.update_dict(a, b)
        self.assertEqual(len(res['t']), 4)
        pass

    def test_update_object_array(self):
        a = {'t': [{'id': 'a1', 'name': 'тест'}, {'id': 'a2', 'name': 'тест'}]}
        b = {'t': [{'id': 'a3', 'name': 'тест'}, {'id': 'a2', 'name': 'тест'}]}
        res = Helper.update_dict(a, b)
        self.assertEqual(len(res['t']), 3)
        pass

    def test_1(self):
        a = {'/oic/con': {
            'rt': ['oic.wk.con', 'bubot.con', 'bubot.VirtualServer.con'], 'if': ['oic.if.baseline'],
            'p': {'bm': 3}, 'logLevel': 'info', 'udpCoapPort': 0, 'udpCoapIPv4': True,
            'udpCoapIPv6': False, 'udpCoapIPv4Ssl': False, 'udpCoapIPv6Ssl': False, 'listening': [],
            'observed': [], 'running_devices': [], 'port': 80}}
        b = {'/oic/d': {'di': '7f9a4170-8c4e-4ca4-939a-70d91a1393b1'}, '/oic/con': {'udpCoapPort': 64682,
                                                                                    'running_devices': [{
                                                                                        'di': '6e356439-104d-4f79-8b78-aed3666463d9',
                                                                                        'dmno': 'SerialServerHF511',
                                                                                        'n': 'Serial server HF511A'}]}}
        res = Helper.update_dict(a, b)
        pass
