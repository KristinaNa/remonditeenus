from django.test import TestCase
from django.models import *

# Create your tests here.
from remont.models import Device


class RemontTestCase(TestCase):
    def setUp(self):
        Device.objects.create(name="ThinkPad", model="5d912")

    def test_device_(self):
        """Animals that can speak are correctly identified"""
        device = Device.objects.values('model').filter(name="ThinkPad")
        self.assertEqual(device[0]['model'], "5d912")
    #
    # def test_index(self):
    #     resp = self.client.get('/polls/')
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertTrue('latest_poll_list' in resp.context)
    #     self.assertEqual([poll.pk for poll in resp.context['latest_poll_list']], [1])