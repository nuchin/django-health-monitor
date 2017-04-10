import json

from django.test import TestCase
from health_monitor.models import Health


class HealthIntegrationTestCase(TestCase):
    def test_post_test_result_int_uid(self):
        # check overall status does not exist
        response = self.client.get('/health/123456789/')
        self.assertEqual(response.status_code, 400)

        # change heart state and severity to 2
        response = self.client.post('/health/123456789/heart/', {'heartrate': 100, 'arrhythmia': 0})
        self.assertNotEqual(response.status_code, 404)
        self.assertContains(response, 'changed to 2')
        health = Health.objects.get(uid=123456789)
        self.assertEqual(health.severity['doctor']['score'], 2)

        # change heart state and severity to 1
        response = self.client.post('/health/123456789/heart/', {'heartrate': 60, 'arrhythmia': 0})
        self.assertNotEqual(response.status_code, 404)
        self.assertContains(response, 'changed to 1')
        health = Health.objects.get(uid=123456789)
        self.assertEqual(health.severity['doctor']['score'], 1)

        # change heart state and severity to 3
        response = self.client.post('/health/123456789/heart/', {'heartrate': 60, 'arrhythmia': 1})
        self.assertNotEqual(response.status_code, 404)
        self.assertContains(response, 'changed to 3')
        health = Health.objects.get(uid=123456789)
        self.assertEqual(health.severity['doctor']['score'], 3)

        # check overall status
        response = self.client.get('/health/123456789/')
        self.assertEqual(response.status_code, 200)

    def test_post_test_result_char_uid(self):
        # check overall status does not exist
        response = self.client.get('/health/joesmith/')
        self.assertEqual(response.status_code, 400)

        # change heart state and severity to 2
        response = self.client.post('/health/joesmith/heart/', {'heartrate': 100, 'arrhythmia': 0})
        self.assertNotEqual(response.status_code, 404)
        self.assertContains(response, 'changed to 2')
        health = Health.objects.get(uid='joesmith')
        self.assertEqual(health.severity['doctor']['score'], 2)

        # change heart state and severity to 1
        response = self.client.post('/health/joesmith/heart/', {'heartrate': 60, 'arrhythmia': 0})
        self.assertNotEqual(response.status_code, 404)
        self.assertContains(response, 'changed to 1')
        health = Health.objects.get(uid='joesmith')
        self.assertEqual(health.severity['doctor']['score'], 1)

        # change heart state and severity to 3
        response = self.client.post('/health/joesmith/heart/', {'heartrate': 60, 'arrhythmia': 1})
        self.assertNotEqual(response.status_code, 404)
        self.assertContains(response, 'changed to 3')
        health = Health.objects.get(uid='joesmith')
        self.assertEqual(health.severity['doctor']['score'], 3)

        # check overall status
        response = self.client.get('/health/joesmith/')
        self.assertEqual(response.status_code, 200)

    def test_delete_asset(self):
        # check 'joesmith' is not in list of uids
        response = self.client.get('/health/')
        self.assertTrue('joesmith' not in json.loads(response.content.decode())['uids'])

        # check overall status does not exist
        response = self.client.get('/health/joesmith/')
        self.assertEqual(response.status_code, 400)

        # post test result to 'joesmith'
        response = self.client.post('/health/joesmith/heart/', {'heartrate': 100, 'arrhythmia': 0})
        self.assertEqual(response.status_code, 200)

        # check 'joesmith' is in list of uids
        response = self.client.get('/health/')
        self.assertTrue('joesmith' in json.loads(response.content.decode())['uids'])

        # delete 'joesmith'
        response = self.client.delete('/health/joesmith/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/health/')
        self.assertTrue('joesmith' not in json.loads(response.content.decode())['uids'])

        # delete nonexistent asset
        response = self.client.delete('/health/joesmith/')
        self.assertEqual(response.status_code, 400)

    def test_update_wrong_test_name(self):
        response = self.client.post('/health/123456789/breath/', {'heartrate': 60, 'arrhythmia': 0})
        self.assertEqual(response.status_code, 400)

    def test_update_wrong_param(self):
        response = self.client.post('/health/123456789/heart/', {'breath': 1})
        self.assertEqual(response.status_code, 400)
