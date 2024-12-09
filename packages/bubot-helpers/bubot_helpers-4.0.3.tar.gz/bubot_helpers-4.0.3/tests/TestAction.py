import time
import unittest

from bubot_helpers.Action import Action
from bubot_helpers.ActionDecorator import action


class TestAction(unittest.TestCase):
    def test_action(self):
        res = 0
        a0 = Action('a0')
        a1 = Action('a1', group='1')
        b1 = Action('b1', group='1')
        a2 = Action('a2', group='2')
        b2 = Action('b2', group='2')
        time.sleep(0.2)
        res += a2.add_stat(a0.set_end(1))
        res += a2.add_stat(b2.set_end(2))
        time.sleep(0.2)
        res += b1.add_stat(a2.set_end(3))
        time.sleep(0.2)
        res += a1.add_stat(b1.set_end(4))
        time.sleep(0.2)
        a1.set_end(res)
        self.assertEqual(8, a1.result)
        self.assertEqual(2, len(list(a1.stat.keys())))
        self.assertEqual(2, len(list(a1.stat['2'].keys())))
        self.assertEqual(2, len(list(a1.stat['1'].keys())))
        pass

    def test_decorator(self):
        test_action = Action('test_decorator')
        res = test_action.add_stat(a1())
        self.assertTrue(res)
        self.assertEqual(2, test_action.stat['a2'][1])
        self.assertEqual(1, test_action.stat['a1'][1])


@action
def a1(_action=None):
    time.sleep(0.1)
    _action.add_stat(a2())
    result = _action.add_stat(a2())
    return _action.set_end(result)


@action
def a2(_action=None):
    time.sleep(0.2)
    return True
