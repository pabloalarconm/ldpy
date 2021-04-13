
# ldpy: Linked Data Platform Client for python.

## New LDP Client to managing meta(data).

### For installing:

 Clone this repo at your computer, move to this folder and install it:
```sh
git clone https://github.com/pabloalarconm/ldpy.git
cd ldpy
python3 setup.py install
```
### First steps:

```python
from ldpy import ldp

#Set a Client object using your endpoint, username and password:
cli=ldp.Client(endpoint="http://Use/your/own/LDP/endpoint/",
                username="username",
                password="password")

```

 **Documentation:** Please check `ldpy/test_package.ipynb` to explore all functionalities inside this package!
