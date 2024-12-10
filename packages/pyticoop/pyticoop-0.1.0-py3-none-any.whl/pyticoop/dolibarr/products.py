from pyticoop.dolibarr.base import DolibarrAPI

class ProductsAPI:
    """
    Gestion des produits via l'API Dolibarr.
    """
    def __init__(self, client: DolibarrAPI):
        self.client = client

    def list_products(self, filters=None):
        """
        Récupère la liste des produits.

        :param filters: Dictionnaire pour filtrer les résultats.
        :return: Liste de produits.
        """
        return self.client.get('/products', params=filters)

    def get_product(self, product_id: int):
        """
        Récupère les détails d'un produit spécifique.

        :param product_id: ID du produit.
        :return: Détails du produit.
        """
        return self.client.get(f'/products/{product_id}')

    def create_product(self, product_data: dict):
        """
        Crée un nouveau produit.

        :param product_data: Dictionnaire contenant les informations du produit.
        :return: Produit créé.
        """
        return self.client.post('/products', json=product_data)

    def update_product(self, product_id: int, product_data: dict):
        """
        Met à jour un produit existant.

        :param product_id: ID du produit.
        :param product_data: Dictionnaire contenant les informations à mettre à jour.
        :return: Produit mis à jour.
        """
        return self.client.put(f'/products/{product_id}', json=product_data)

    def delete_product(self, product_id: int):
        """
        Supprime un produit.

        :param product_id: ID du produit.
        :return: Résultat de l'opération.
        """
        return self.client.delete(f'/products/{product_id}')
