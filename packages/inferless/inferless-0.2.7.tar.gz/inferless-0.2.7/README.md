# Python Client to call Inferless API

## Installation
```console
$ pip install inferless
```

## Usage
This client can be used to call Inferless API from your python code. It supports both synchronous and asynchronous calls.
### Constants
Fetch the URL and API_KEY from the Inferless console https://console-dev.inferless.com/
```python
URL = "<url>"
API_KEY = "<api_key>"
```

### Input Data
Input data can be provided in two formats, as shown below as inputs and data.
```python
INPUTS = { "inputs" : 
          [
              {
                "name": "prompt",
                "shape": [
                  1
                ],
                "datatype": "BYTES",
                "data": [
                  "Once upon a time"
                ]
              }
          ]
        }
```

This other format is simpler and can be used if other parameters are not required. `datatype` and `shape` are automatically inferred.
```python
DATA = {
    "prompt": "Once upon a time"
}
```

### Synchrounous call
An example to call Inferless API synchronously
```python
import inferless
import datetime
def main():
    t1 = datetime.datetime.now()
    data = inferless.call(url=URL, workspace_api_key=API_KEY, inputs=INPUTS)
    t2 = datetime.datetime.now()
    print(f"time taken: {t2-t1}")

main()
```
Output
```console
time taken: 0:00:05.218835
```
For a particular url, the synchronous call took approximately 5 seconds to complete.

### Async call with callback
This library also supports async calls to Inferless API. The following example shows how to call Inferless API in background with a callback function.
```python
import inferless
import datetime

def callback_func(e, response):
    # e is the error object
    # response is the response object
    with open("response.json", "w") as f:
        f.write(json.dumps(response))
    

t1 = datetime.now()
inferless.call_async(url=URL, workspace_api_key=KEY, data=data, callback=callback_func)
t2 = datetime.now()
print(t2 - t1)
```
Output
```console
time taken: 0:00:00.000141
```
It can be seen that the program continues without waiting for the response. The response is written to a file by the callback function after it is received.

### Batch call
If the model is configured for batch processing, `is_batch` should be set to `True`