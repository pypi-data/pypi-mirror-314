import unittest
from unittest.mock import MagicMock
import requests_mock
from pyticoop.dolibarr.base import DolibarrAPI
from pyticoop.dolibarr.products import ProductsAPI

class TestProductsAPI(unittest.TestCase):

    def setUp(self):
        # Initialisation du client API et de l'API des produits
        self.api_client = DolibarrAPI(base_url="https://example.com/api/index.php", api_key="fake_api_key")
        self.products_api = ProductsAPI(self.api_client)

    @requests_mock.Mocker()
    def test_list_products(self, mock):
        # Simuler la réponse d'une liste de produits
        mock.get("https://example.com/api/index.php/products", json={"data": ["product1", "product2"]}, status_code=200)
        
        # Appel de la méthode list_products
        response = self.products_api.list_products()
        
        # Vérification de la réponse
        self.assertEqual(response, {"data": ["product1", "product2"]})

    @requests_mock.Mocker()
    def test_get_product(self, mock):
        # Simuler la réponse pour la récupération d'un produit spécifique
        mock.get("https://example.com/api/index.php/products/1", json={"id": 1, "ref": "PROD001"}, status_code=200)
        
        # Appel de la méthode get_product
        response = self.products_api.get_product(1)
        
        # Vérification de la réponse
        self.assertEqual(response, {"id": 1, "ref": "PROD001"})

    @requests_mock.Mocker()
    def test_create_product(self, mock):
        # Simuler la réponse pour la création d'un produit
        new_product = {"ref": "PROD001", "label": "New Product", "price": 100}
        mock.post("https://example.com/api/index.php/products", json={"id": 123, "ref": "PROD001"}, status_code=201)
        
        # Appel de la méthode create_product
        response = self.products_api.create_product(new_product)
        
        # Vérification de la réponse
        self.assertEqual(response, {"id": 123, "ref": "PROD001"})

    @requests_mock.Mocker()
    def test_update_product(self, mock):
        # Simuler la réponse pour la mise à jour d'un produit
        updated_product = {"ref": "PROD001_UPDATED", "label": "Updated Product", "price": 120}
        mock.put("https://example.com/api/index.php/products/123", json={"ref": "PROD001_UPDATED"}, status_code=200)
        
        # Appel de la méthode update_product
        response = self.products_api.update_product(123, updated_product)
        
        # Vérification de la réponse
        self.assertEqual(response, {"ref": "PROD001_UPDATED"})

    @requests_mock.Mocker()
    def test_delete_product(self, mock):
        # Simuler la réponse pour la suppression d'un produit
        mock.delete("https://example.com/api/index.php/products/123", status_code=204)
        
        # Appel de la méthode delete_product
        response = self.products_api.delete_product(123)
        
        # Vérification de la réponse
        self.assertEqual(response, '')

if __name__ == '__main__':
    unittest.main()
