import unittest
from unittest.mock import patch, MagicMock
from pyonix import IonixClient

class TestIonixClient(unittest.TestCase):
    def setUp(self):
        self.client = IonixClient(
            base_url="https://api.portal.ionix.io/api/v1",
            api_token="test-token",
            account_name="test-account"
        )

    def test_init(self):
        """Test client initialization"""
        self.assertEqual(self.client.base_url, "https://api.portal.ionix.io/api/v1")
        self.assertEqual(self.client.headers["Authorization"], "Bearer test-token")
        self.assertEqual(self.client.headers["X-Account-Name"], "test-account")

    @patch('requests.Session.get')
    def test_get(self, mock_get):
        """Test GET request"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response

        result = self.client.get("test/endpoint")
        
        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once()

if __name__ == '__main__':
    unittest.main()
