import requests
import aiohttp
import json
from anura.direct.result import DirectResult
from anura.direct.exceptions import AnuraException, AnuraClientException, AnuraServerException
from typing import Awaitable

class AnuraDirect:
    """
    An Anura Direct API client.
    """

    __instance = ''
    __source = ''
    __campaign = ''
    __additional_data = {}
    __use_https = True

    def __init__(self, instance: str, use_https: bool = True):
        self.__instance = instance
        self.__use_https = use_https

    def get_result(self, ip_address: str, user_agent: str = '', app: str = '', device: str = '') -> DirectResult:
        """
        Gets a result from Anura Direct, or raises an exception if an error occurred.
        """
        params = {
            'instance': self.__instance,
            'ip': ip_address
        }

        if (self.__source):
            params['source'] = self.__source
        if (self.__campaign):
            params['campaign'] = self.__campaign
        if (user_agent):
            params['ua'] = user_agent
        if (app):
            params['app'] = app
        if (device):
            params['device'] = device
        if (len(self.__additional_data) > 0):
            params['additional'] = self.__get_additional_data_string()

        response = requests.get(self.__get_url(), params)

        is_server_error = response.status_code in range(500, 600)
        if is_server_error:
            raise AnuraServerException("Anura Server Error: " + response.status_code)

        try:
            result = response.json()
        except:
            raise AnuraException("Unknown error occurred")

        is_client_error = response.status_code in range(400, 500)
        if is_client_error:
            raise AnuraClientException(result['error'] or 'Client side error occurred')

        direct_result = DirectResult(result['result'], result['mobile'])
        if 'rule_sets' in result:
            direct_result.rule_sets = result['rule_sets']
        if 'invalid_traffic_type' in result:
            direct_result.invalid_traffic_type = result['invalid_traffic_type']

        return direct_result

    async def get_result_async(self, session: aiohttp.ClientSession, ip_address: str, user_agent: str = '', app: str = '', device: str = '') -> Awaitable[DirectResult]:
        """
        Asynchronously gets a result from Anura Direct, or raises an exception if an error occurred.
        """

        params = {
            'instance': self.__instance,
            'ip': ip_address
        }

        if (self.__source):
            params['source'] = self.__source
        if (self.__campaign):
            params['campaign'] = self.__campaign
        if (user_agent):
            params['ua'] = user_agent
        if (app):
            params['app'] = app
        if (device):
            params['device'] = device
        if (len(self.__additional_data) > 0):
            params['additional'] = self.__get_additional_data_string()

        async with session as client:
            async with client.get(url=self.__get_url(), params=params) as response:
                is_server_error = response.status in range(500, 600)
                if is_server_error:
                    raise AnuraServerException("Anura Server Error: " + response.status)
                
                try:
                    result = await response.json()
                except:
                    raise AnuraException("Unknown error occurred")

                is_client_error = response.status in range(400, 500)
                if is_client_error:
                    raise AnuraClientException(result['error'] or 'Client error occurred')
                
                direct_result = DirectResult(result['result'], result['mobile'])
                if 'rule_sets' in result:
                    direct_result.rule_sets = result['rule_sets']
                if 'invalid_traffic_type' in result:
                    direct_result.invalid_traffic_type = result['invalid_traffic_type']
                
                return direct_result

    @property
    def instance(self) -> str:
        return self.__instance
    
    @instance.setter
    def instance(self, instance: str) -> None:
        self.__instance = instance

    @property
    def source(self) -> str:
        return self.__source
    
    @source.setter
    def source(self, source: str) -> None:
        self.__source = source

    @property
    def campaign(self) -> str:
        return self.__campaign
    
    @campaign.setter
    def campaign(self, campaign: str) -> None:
        self.__campaign = campaign

    @property
    def additional_data(self) -> dict:
        return self.__additional_data

    @additional_data.setter
    def additional_data(self, additional_data: dict) -> None:
        self.__additional_data = additional_data
    
    def add_additional_data(self, key: str, value: str) -> None:
        """
        Adds a key/value pair to your additional data. If you call 
        this method providing the same key multiple times, the element 
        at that index will be updated with your new value.
        """

        self.__additional_data[key] = value

    def remove_additional_data(self, key: str) -> None:
        """
        Removes a key/value pair from Anura Direct's additional data.
        """

        if key in self.__additional_data:
            del self.__additional_data[key]

    def __get_url(self) -> str:
        if (self.__use_https):
            return 'https://direct.anura.io/direct.json'
        else:
            return 'http://direct.anura.io/direct.json'
        
    def __get_additional_data_string(self) -> str:
        if (len(self.__additional_data) <= 0):
            return ''
        
        additional_data_string = json.dumps(self.__additional_data)
        return additional_data_string