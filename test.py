import unittest
from app import app

class ContactListAPITest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        # Create a new contact for testing purposes
        response = self.app.post('/contacts', data={'name': 'John Doe', 'phone_numbers': ['1234567890']})
        self.assertEqual(response.status_code, 201)
        # Extract the ID of the newly created contact from the response
        self.contact_id = response.get_data(as_text=True)  # Get the contact ID from response text

    def test_fetch_all_contacts(self):
        response = self.app.get('/contacts')
        self.assertEqual(response.status_code, 200)

    def test_search_contacts(self):
        response = self.app.get('/contacts/search?name=John')
        self.assertEqual(response.status_code, 200)

    def test_update_existing_contact(self):
        # Use the ID of the newly created contact for updating
        response = self.app.put(f'/contacts/{self.contact_id}', data={'name': 'Updated Name', 'phone_numbers': ['9876543210']})
        self.assertEqual(response.status_code, 200)

    def test_delete_existing_contact(self):
        # Use the ID of the newly created contact for deletion
        response = self.app.delete(f'/contacts/{self.contact_id}')
        self.assertEqual(response.status_code, 200)

    def test_export_contacts_to_csv(self):
        response = self.app.get('/contacts/export/csv')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
