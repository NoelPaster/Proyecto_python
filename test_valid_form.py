import unittest
from valid_form import valid_form

class TestValidForm(unittest.TestCase):
    def test_valid_form(self):
        result = valid_form(
            username="Maria",
            password="marianoel"
        )
        self.assertTrue(result)
        result = valid_form(
            username="Maria",
            password="noel"
        )
        self.assertFalse(result)


