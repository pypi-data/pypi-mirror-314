from scrapeanything.types.requests import Methods
from scrapeanything.types.requests import ResponseTypes
import requests

class ApiService:

    def wget(self, url: str, parameters: dict=None, method: Methods=Methods.GET, response_type: ResponseTypes=ResponseTypes.JSON) -> any:
        if method == Methods.GET:
            response = requests.get(url=url, data=parameters)
        elif method == Methods.POST:
            response = requests.post(url=url, data=parameters)
        else:
            raise Exception(f'{method} method is not supported')

        if response_type == ResponseTypes.JSON:
            return response.json()
        elif response_type == ResponseTypes.TEXT:
            return response.text
        else:
            raise Exception(f'{response_type} response type is not supported')