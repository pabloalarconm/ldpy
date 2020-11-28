
# ldpy: Linked Data Platform Client for python.

### New LDP Client to managing meta(data).

## For installing:

 Clone this repo at your computer, move to this folder and install it:
```bash
python3 setup.py install
```
## First step:

```python
from ldpy import ldp

#Set a Client object using your endpoint, username and password:
cli=ldp.Client(endpoint="http://Use/your/own/LDP/endpoint/",
                username="username",
                password="password")

```
### There a test_package.ipynb as test with all functionalities inside this package as Docs to learn more about how to use it. Please take a look!

