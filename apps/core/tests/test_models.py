from django.test import TestCase


class DummyTestCase(TestCase):
    def setUp(self):
        super().setUp()

    def test_unittest_engine(self):
        self.assertEqual(True, True)
