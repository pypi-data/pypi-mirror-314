import requests
from requests.exceptions import HTTPError, Timeout, RequestException
from muslimDeen.config import Config
from typing import Union


class Services:
    def __init__(self) -> None:
        pass

    def request_services(self, url: str, to_json: bool = False, to_text: bool = False) -> Union[dict, str, requests.Response]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            if to_json:
                return response.json()
            elif to_text:
                return response.text
            else:
                return response

        except HTTPError as http_err:
            raise Exception(f"HTTPError: {http_err}")
        except Timeout:
            raise Exception("Request timeout")
        except RequestException as req_err:
            raise Exception(f"RequestException: {req_err}")
        except Exception as e:
            raise Exception(f"General error: {e}")

    def metadata_off_surahs(self) -> dict:
        return self.request_services(Config.url_meta_data_v1(), to_json=True)

    def quran_to_json(self) -> dict:
        return self.request_services(Config.url_data_quran(), to_json=True)

    def dictionnary_to_dic(self) -> str:
        return self.request_services(Config.dictionnary_fr(), to_text=True)
