# Anura SDK for Python

The **Anura SDK for Python** makes it easy for developers to access Anura Direct within their Python code, and begin analyzing their traffic. You can get started in minutes by installing the SDK from PyPI or our source code.

## Getting Started
1. **Have an open active account with Anura**. You can see more about Anura's offerings [here.](https://www.anura.io/product#plans-pricing)
2. **Minimum Requirements** - To use the SDK, you will need **Python >=3.10**.
3. **Install the SDK** - Using **pip** is the easiest and recommended way to install it. You can install it with the following command:
```sh
pip install anura
```
Or, install from source by using one of the following examples according to your operating system:

Linux/Mac:
```sh
git clone https://github.com/anuraio/anura-sdk-python.git
cd anura-sdk-python
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
```

Windows:
```sh
git clone https://github.com/anuraio/anura-sdk-python.git
cd anura-sdk-python
py -m pip install -r requirements.txt
py -m pip install -e .
```

4. View our [**Quick Examples**](#quick-examples) to immediately begin using the SDK!

## Quick Examples
### Create the Anura Direct Client
```python
from anura.direct.client import AnuraDirect

direct = AnuraDirect('your-instance-id-goes-here')
```
### Set a custom source, campaign, and additional data for Anura Direct
```python
direct.source = 'your-source-value'
direct.campaign = 'your-campaign-value'
direct.add_additional_data('1', 'your-data-value')
```

### Updating additional data at a specific index
```python
# To update an element of additional data at a specific index,
# simply add the element again but with a new value.
index_to_update = '1'
direct.add_additional_data(index_to_update, 'your-new-data-value')
```

### Removing an element from additional data
```python
index_to_remove = '1'
direct.remove_additional_data(index_to_remove)
```

### Get a result from Anura Direct
```python
try:
    result = direct.get_result(
        'visitors-ip-address', # required
        'visitors-user-agent', # optional
        'visitors-app-package-id', # optional
        'visitors-device-id' # optional
    )
    print('result: ' + str(result))
except Exception as e:
    print(e)
```

### Get a result from Anura Direct asynchronously
```python
import asyncio
import aiohttp

async def main():
    direct = AnuraDirect('your-instance-id')

    async with aiohttp.ClientSession() as session:
        try:
            result = await direct.get_result_async(
                session, # required
                'visitors-ip-address', # required
                'visitors-user-agent', # optional
                'visitors-app-package-id', # optional
                'visitors-device-id' # optional
            )
            print('result: ' + str(result))
        except Exception as e:
            print(e)

asyncio.run(main())
```


## API Reference
### AnuraDirect
Can get results from Anura Direct. These results are fetched using Direct's `/direct.json` API endpoint.

#### Methods
**`get_result() -> DirectResult`**
- Gets a result synchronously from Anura Direct. Raises an exception if an error occurs throughout the result fetching process.
- Exceptions thrown:
    - `AnuraException`: if a 4XX, 5XX, or any unknown response is returned from Anura Direct

Parameters:
| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| `ip_address` | `str` | The IP address of your visitor. Both IPv4 & IPv6 addresses are supported. | Yes |
| `user_agent` | `str` | The user agent string of your visitor | |
| `app` | `str` | The application package identifier of your visitor (when available.) | |
| `device` | `str` | The device identifier of your visitor (when available.) | |


**`get_result_async() -> Awaitable[DirectResult]`**
- Gets a result asynchronously from Anura Direct. Raises an exception if an error occurs throughout the result fetching process.
- Exceptions thrown:
    - `AnuraException`: if a 4XX, 5XX, or any unknown response is returned from Anura Direct

Parameters:
| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| `session` | `aiohttp.ClientSession` | The aiohttp client session object | Yes |
| `ip_address` | `str` | The IP address of your visitor. Both IPv4 & IPv6 addresses are supported. | Yes |
| `user_agent` | `str` | The user agent string of your visitor | |
| `app` | `str` | The application package identifier of your visitor (when available.) | |
| `device` | `str` | The device identifier of your visitor (when available.) | |

**`add_additional_data(self, key: str, value: str) -> None`**
- Adds an element of additional data to your `AnuraDirect` client.

**`remove_additional_data(self, key: str) -> None`**
- Removes the element of your additional data array located at the provided `key`.

**`@property instance(self) -> str`**
- Returns the instance you have set within the `AnuraDirect` client.

**`@property source(self) -> str`**
- Returns the source you have set within the `AnuraDirect` client.

**`@property campaign(self) -> str`**
- Returns the campaign you have set within the `AnuraDirect` client.

**`@property additional_data(self) -> dict`**
- Returns the additional data you have set within the `AnuraDirect` client.

**`@instance.setter instance(self, instance: str) -> None`**
- Sets the Instance ID of the `AnuraDirect` client to the `instance` value passed.

**`@source.setter source(self, source: str) -> None`**
- Sets the source of the `AnuraDirect` client to the `source` value passed.

**`@campaign.setter campaign(self, campaign: str) -> None`**
- Sets the campaign of the `AnuraDirect` client to the `campaign` value passed.

**`@additional_data.setter additional_data(self, additional_data: dict) -> None`**
- Sets the additional data of the `AnuraDirect` client to the `additional_data` value passed.

### DirectResult
The result upon a successful call to `get_result()` or `get_result_async()` from the `AnuraDirect` client. It contains not only the result from Anura Direct, but some other methods to help you use the result as well.

#### Methods
**`is_suspect() -> bool`**
- Returns whether or not the visitor has been determined to be **suspect**.

**`is_non_suspect() -> bool`**
- Returns whether or not the visitor has been determined to be **non-suspect**.

**`is_mobile() -> bool`**
- Returns whether or not the visitor has been determined to be on a mobile device.

#### Properties
**`result: str`**
- Besides using the `is_suspect()` or `is_non_suspect()` methods, you are also able to directly access the result value.

**`rule_sets: str[] | None`**
- If you have **return rule sets** enabled, you will be able to see which specific rules were violated upon a **suspect** result. This value will be `None` if the visitor is **non-suspect**, or if you do not have **return rule sets** enabled.
- You can talk to [support](mailto:support@anura.io) about enabling or disabling the **return rule sets** feature.

**`invalid_traffic_type: str | None`**
- If you have **invalid traffic type** enabled, you will be able to access which type of invalid traffic occurred upon a **suspect** result.
- You can talk to [support](mailto:support@anura.io) about enabling or disabling the **return invalid traffic type** feature.
