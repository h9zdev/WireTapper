import unittest
import importlib
import app

class TestSDRIntegration(unittest.TestCase):
    def setUp(self):
        self.app_client = app.app.test_client()
        app_env = importlib.import_module('app-env')
        self.app_env_client = app_env.app.test_client()

    def test_sdr_status_endpoint(self):
        for client in [self.app_client, self.app_env_client]:
            response = client.get('/api/sdr/status')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('connected', data)
            self.assertIn('device', data)
            self.assertIn('frequency_range', data)

    def test_nearby_sdr_mode(self):
        for client in [self.app_client, self.app_env_client]:
            response = client.get('/nearby?lat=51.505&lon=-0.09&mode=sdr')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('devices', data)
            self.assertIn('sdr_status', data)
            self.assertGreater(len(data['devices']), 0)
            for dev in data['devices']:
                self.assertEqual(dev['type'], 'sdr')

    def test_search_sdr_mode(self):
        for client in [self.app_client, self.app_env_client]:
            response = client.get('/searchzz?type=ssid&query=433MHz&mode=sdr')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('devices', data)
            self.assertIn('sdr_status', data)
            self.assertGreater(len(data['devices']), 0)
            self.assertEqual(data['devices'][0]['type'], 'sdr')

if __name__ == '__main__':
    unittest.main()
