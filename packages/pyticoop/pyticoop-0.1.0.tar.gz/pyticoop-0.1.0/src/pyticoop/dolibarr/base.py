import requests

class DolibarrAPI:
    """
    Client pour interagir avec l'API Dolibarr.
    """
    def __init__(self, base_url: str, api_key: str):
        """
        Initialise le client API.

        :param base_url: URL de base de l'API Dolibarr (exemple : https://example.com/api/index.php).
        :param api_key: Clé API pour authentification.
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'DOLAPIKEY': api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def _request(self, method: str, endpoint: str, **kwargs):
        """
        Envoie une requête HTTP générique à l'API.

        :param method: Méthode HTTP (GET, POST, PUT, DELETE).
        :param endpoint: Endpoint spécifique (exemple : /products).
        :return: Réponse JSON ou lève une exception en cas d'erreur.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.request(method, url, headers=self.headers, **kwargs)

        if not response.ok:
            raise Exception(f"Erreur API ({response.status_code}): {response.text}")
        
        try:
            return response.json()
        except ValueError:
            return response.text

    def get(self, endpoint: str, params=None):
        return self._request('GET', endpoint, params=params)

    def post(self, endpoint: str, json=None):
        return self._request('POST', endpoint, json=json)

    def put(self, endpoint: str, json=None):
        return self._request('PUT', endpoint, json=json)

    def delete(self, endpoint: str):
        return self._request('DELETE', endpoint)
