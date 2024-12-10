import unittest
import requests
import requests_mock
from pyticoop.dolibarr.base import DolibarrAPI

class TestDolibarrAPI(unittest.TestCase):

    def setUp(self):
        # Initialisation du client API avec une URL fictive
        self.api = DolibarrAPI(base_url="https://example.com/api/index.php", api_key="fake_api_key")

    @requests_mock.Mocker()
    def test_get_request_success(self, mock):
        # Simuler une réponse pour une requête GET
        mock.get("https://example.com/api/index.php/products", json={"data": ["product1", "product2"]}, status_code=200)
        
        # Appel à la méthode GET
        response = self.api.get("/products")
        
        # Vérifier la réponse
        self.assertEqual(response, {"data": ["product1", "product2"]})
    
    @requests_mock.Mocker()
    def test_get_request_failure(self, mock):
        # Simuler une réponse d'erreur pour une requête GET
        mock.get("https://example.com/api/index.php/products", status_code=404)
        
        # Appel à la méthode GET et vérification de l'exception
        with self.assertRaises(Exception) as context:
            self.api.get("/products")
        
        self.assertTrue('Erreur API' in str(context.exception))

    @requests_mock.Mocker()
    def test_post_request(self, mock):
        # Simuler une réponse pour une requête POST
        mock.post("https://example.com/api/index.php/products", json={"id": 123, "ref": "PROD001"}, status_code=201)
        
        # Appel à la méthode POST
        new_product = {"ref": "PROD001", "label": "Product 1", "price": 50}
        response = self.api.post("/products", json=new_product)
        
        # Vérifier la réponse
        self.assertEqual(response, {"id": 123, "ref": "PROD001"})

    @requests_mock.Mocker()
    def test_put_request(self, mock):
        # Simuler une réponse pour une requête PUT
        mock.put("https://example.com/api/index.php/products/123", json={"ref": "PROD001_UPDATED"}, status_code=200)
        
        # Appel à la méthode PUT
        updated_product = {"ref": "PROD001_UPDATED", "label": "Product 1 Updated", "price": 60}
        response = self.api.put("/products/123", json=updated_product)
        
        # Vérifier la réponse
        self.assertEqual(response, {"ref": "PROD001_UPDATED"})

    @requests_mock.Mocker()
    def test_delete_request(self, mock):
        # Simuler une réponse pour une requête DELETE
        mock.delete("https://example.com/api/index.php/products/123", status_code=204)
        
        # Appel à la méthode DELETE
        response = self.api.delete("/products/123")
        
        # Vérifier la réponse
        self.assertEqual(response, '')

if __name__ == '__main__':
    unittest.main()
