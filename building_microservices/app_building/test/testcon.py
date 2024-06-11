import os
import sys
import unittest

# Set up the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)    # Adding the parent directory to the system path
sys.path.append(grandparent_dir)  # Adding the grandparent directory to the system path

# Now we can safely import create_app from run
from building_microservices.run import create_app

class TestControllers(unittest.TestCase):

    def setUp(self):
        # Create the app using the create_app factory function
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_address(self):
        # Make a GET request to the route
        response = self.client.get('/address', query_string={'address': 'Kærvej 7, 9800'})
        
        # Assert the response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('vejnavn', data)
        self.assertIn('husnr', data)
        self.assertIn('postnr', data)
        self.assertIn('postnrnavn', data)
        self.assertIn('tekst', data)

    def test_get_address_missing_parameter(self):
        # Make a GET request without the required parameter
        response = self.client.get('/address')
        
        # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Address parameter is required'})

    def test_get_address_details(self):
        # Known valid address ID for testing
        address_id = "0a3f50c8-2902-32b8-e044-0003ba298018"
        
        # Make a GET request to the route
        response = self.client.get(f'/address/{address_id}')
        
        # Assert the response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertIn('vejnavn', data)
        self.assertIn('husnr', data)
        self.assertIn('postnr', data)
        self.assertIn('postnrnavn', data)

    def test_get_building_details(self):
        # Known valid building ID for testing
        building_id = "3d90f674-e642-4516-b4a1-45f2617b561f"
        
        # Make a GET request to the route
        response = self.client.get(f'/building/{building_id}')
        
        # Assert the response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('id_lokalId', data)
        self.assertIn('byg007Bygningsnummer', data)
        self.assertIn('byg021BygningensAnvendelse', data)
        self.assertIn('byg026Opførelsesår', data)
        self.assertIn('byg032YdervæggensMateriale', data)
        self.assertIn('byg033Tagdækningsmateriale', data)

if __name__ == '__main__':
    unittest.main()
