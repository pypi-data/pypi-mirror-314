import requests
import os
import threading
from enum import Enum
from datetime import datetime, timezone
from requests.exceptions import ConnectionError, Timeout, RequestException
import time
import sys

sys.setrecursionlimit((20 * 10000000)) # Até 20 milhões

# TODO: Remover hardcode chaves e segredos
# Parâmetros que devem ser configurados através de variáveis de comando.
BONANZA_SAP_API_URL = os.environ.get("BONANZA_SAP_API_URL")
BONANZA_SAP_API_KEY = os.environ.get("BONANZA_SAP_API_KEY")
BONANZA_SAP_API_USERNAME = os.environ.get("BONANZA_SAP_API_USERNAME")
BONANZA_SAP_API_PASSWORD = os.environ.get("BONANZA_SAP_API_PASSWORD")
BONANZA_SAP_API_COMPANY_DB = os.environ.get("BONANZA_SAP_API_COMPANY_DB")

def sap_formatted_query_date(base_date : datetime) -> str:
    """ Retornar uma string que representa uma data formatada para utilizar como filtro """
    base_date_utc = base_date.replace(tzinfo=timezone.utc)
    fd = base_date_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    return fd

class SapApiException(Exception):
    """ Exceção padrão de erro do SAP """

    def __init__(self, message : str, code : int):
        """ Construtor padrão """
        self.message = message
        self.code = code
        super().__init__(self.message)

class SapApiConnection:

    _instance = None
    _session_id = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SapApiConnection, cls).__new__(cls)
        return cls._instance

    def _connect(self) -> str:

        headers = {
            "Content-Type": "application/json",
            "apikey": BONANZA_SAP_API_KEY
        }

        body = {
            "CompanyDB": BONANZA_SAP_API_COMPANY_DB,
            "Password": BONANZA_SAP_API_PASSWORD,
            "UserName": BONANZA_SAP_API_USERNAME
        }

        r = requests.post(f"{BONANZA_SAP_API_URL}/Login", headers=headers, json=body, verify=False)

        if r.status_code == 200:
            return "; ".join(["".join([k.name, "=", k.value]) for k in r.cookies])
        else:
            raise SapApiException(r.text, r.status_code)

    def get_session_id(self, force_reconnection = False) -> str:
        """
        Efetuar a conexão com a API do SAP e retornar o session id
        """
        with SapApiConnection._lock:
            if force_reconnection:
                SapApiConnection._session_id = None
            if SapApiConnection._session_id is None:
                SapApiConnection._session_id = self._connect()
        return SapApiConnection._session_id

class SapApiRequestMethod(Enum):
    POST = 1,
    GET = 2

class SapApiRequest:

    _methods = {
        SapApiRequestMethod.GET: requests.get,
        SapApiRequestMethod.POST: requests.post
    }

    def __init__(self, request_method : SapApiRequestMethod, api_query : str, **kwargs):
        """ Construtor padrão """
        self.request_method = request_method
        self.api_query = api_query
        self.body = kwargs.get("body")

    def get_api_url(self):
        return f"{BONANZA_SAP_API_URL}/{self.api_query}"

    def request_data(self, connection : SapApiConnection, url : str, **kwargs) -> dict:
        """ Executar a requisição dos dados """
        force_reconnection = kwargs.get("force_reconnection", False)

        f = SapApiRequest._methods.get(self.request_method)

        if f is None or not callable(f):
            raise SapApiException("Método inválido!", -1)
        
        MAX_RETRIES = 3
        attempt = 0
        last_error = None

        while True:
            attempt += 1

            try:

                headers = {
                    "Cookie": connection.get_session_id(force_reconnection=force_reconnection)
                }

                body = self.body

                params = {
                    "url": url,
                    "headers": headers,
                    "verify": False,
                    "timeout": 240
                }

                if body:
                    if type(body) is dict:
                        params['json'] = body
                    else:
                        params['data'] = body

                r = f(**params)

                if r.status_code == 200:
                    attempt = 0 # 21/10/24 - Ajuste CVB
                    return r.json()
                
                elif r.status_code == 401:
                    error_data = r.json()
                    error = error_data.get("error")
                    if error:
                        error_code = error.get("code")
                        if error_code == 301 and not force_reconnection:
                            time.sleep(5)
                            force_reconnection = True
                            if attempt > 0:
                                attempt -= 1
                            continue

                raise SapApiException(r.text, r.status_code)
            
            except (SapApiException, ConnectionError, TimeoutError, RequestException) as e: # 21/10/24 - Ajuste CVB, incluir SapApiException
                last_error = e
                print(f"request_data: attempt {attempt}, error {e}")
                time.sleep(5)

            if attempt >= MAX_RETRIES:
                if not last_error is None:
                    raise last_error
                else:
                    break

        raise SapApiException("Falha execução", -1)


        
class SapApiPaginationRequest(SapApiRequest):

    def __init__(self, request_method : SapApiRequestMethod, api_name : str, **kwargs):
        self._api_filter = kwargs.get("api_filter")
        self._api_order_by = kwargs.get("api_order_by")
        self._api_select = kwargs.get("api_select")
        self._api_skip = kwargs.get("api_skip")
        self._api_top = kwargs.get("api_top")

        api_query_pagination = api_name
        parameters = []

        if self._api_filter != None and str(self._api_filter).strip() != "":
            parameters.append(f"$filter={str(self._api_filter).strip()}")
        if self._api_order_by != None and str(self._api_order_by).strip() != "":
            parameters.append(f"$orderBy={str(self._api_order_by).strip()}")
        if self._api_select != None and str(self._api_select).strip() != "":
            parameters.append(f"$select={str(self._api_select).strip()}")
        if self._api_skip != None and int(self._api_skip) != 0:
            parameters.append(f"$skip={int(self._api_skip)}")
        if self._api_top != None and int(self._api_top) != 0:
            parameters.append(f"$top={int(self._api_top)}")

        api_query_parameters = "&".join(parameters)
        if api_query_parameters != None and str(api_query_parameters).strip() != "":
            api_query_pagination += ("?" + api_query_parameters)

        super().__init__(request_method=request_method, api_query=api_query_pagination, kwargs=kwargs)

    def request_paginate_data(self, connection : SapApiConnection, **kwargs) -> iter:
        """ Retornar dados paginados """
        url = kwargs.get("url")
        if url is None or str(url).strip() == "":
            url = self.get_api_url()

        data = self.request_data(connection=connection, url=url)

        if data:
            yield data
            
            url_next_page = data.get("odata.nextLink")
            if url_next_page:
                yield from self.request_paginate_data(connection=connection, url=f"{BONANZA_SAP_API_URL}/{url_next_page}")
