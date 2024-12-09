import unittest

from Bubot.Helpers.Action import Action
from Bubot.Helpers.ExtException import ExtException, NotAvailable


class TestExtException(unittest.TestCase):
    def test_raise_from_other_ext_exception(self):
        try:
            try:
                err1 = ExtException(message='msg1', action='action1')
                raise err1
            except ExtException as err:
                err2 = ExtException(message='msg2', action='action2', parent=err)
                raise err2
        except ExtException as err:
            err3 = ExtException(action='action3', parent=err)
        self.assertEqual(2, len(err3.stack))
        self.assertEqual('msg1', err3.stack[0]['message'])
        self.assertEqual('msg2', err3.message)
        print(err3)

    def test_raise_from_with_action(self):
        res = Action('action1')
        res2 = Action('action2')
        res2.add_stat(Action('action3').set_end())

        try:
            try:
                err1 = ExtException(message='msg1', action=res2)
                raise err1
            except ExtException as err:
                err2 = ExtException(message='msg2', action=res, parent=err)
                raise err2
        except ExtException as err:
            err3 = ExtException(action='action3', parent=err)
        self.assertEqual(2, len(err3.stack))
        self.assertEqual('msg1', err3.stack[0]['message'])
        self.assertEqual('msg2', err3.message)
        print(err3)

    def test_loads_exception(self):
        res = ExtException(
            parent={
                "__module__": "Bubot.Helpers.ExtException",
                "__name__": "NotAvailable",
                "message": "test",
                "stack": [{"action": 1}]
            }
        )
        self.assertIsInstance(res, NotAvailable)
        self.assertEqual(1, len(res.stack))
        pass

    def test_raise_from_other_ext_exception_type(self):
        try:
            try:
                err1 = NotAvailable(message='msg1', action='action1')
                raise err1
            except ExtException as err:
                err2 = ExtException(message='msg2', action='action2', parent=err)
                raise err2
        except ExtException as err:
            err3 = ExtException(action='action3', parent=err)
        self.assertEqual(2, len(err3.stack))
        self.assertEqual('msg1', err3.stack[0]['message'])
        self.assertEqual('msg2', err3.message)
        print(err3)
