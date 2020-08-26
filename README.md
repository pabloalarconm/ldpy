
## ldpy: Linked Data Platform Client for python

```python
import os
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD, RDF
import re
import sys
import requests

from ldpy import ldp

```
### Set main parameter:

```python
#Set client class
cli=ldp.Client(endpoint="http://Use/your/own/LDP/endpoint/",
                username="username",
                password="password")

# set container object:
cont=cli.containers_level

```
### Create a new container:

```python
cont.addnewcontainer(location="parent_container", 
                        slug="NewContainer") #you can choice as location any container inside the parent container (endpoint) as well.

```
### Add metadata to containers:

```python
# By using rdflib module:
pablo = URIRef("http://example.org/pablo")

cont.add_metadata_to_Cont("NewContainer",g=[[pablo,FOAF.name,"Pablo Alarcon"],
                                     [pablo,RDF.type, FOAF.Person]])
#For delete it:                                  
cont.delete("NewContainer")

```
### Delete Containers:

```python
cont.delete("NewContainer")
```

### Set resource object based on container object:

```python
res=cont.resources_level
```

### Create new resource 
```python
res.addnewresource(location="NewContainer",
                       slug="NewResource",
                        g=graph) #g parameter must be a graph object or a list of triples as: [[s,p,o],[s,p,o],[s,p,o]]
```

### Add metadata to Resources



```python
pablo = URIRef("http://example.org/pablo")

res.add_metadata_to_Res("NewResource",g=[[pablo,FOAF.name,"Pablo Alarcon"],
                                     [pablo,RDF.type, FOAF.Person]])


```

### Delete Containers:

```python
cont.delete("NewContainer")
```





