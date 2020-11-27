from rdflib import Graph, Literal, RDF, URIRef
import re
import sys
import requests

from ldpy.util import httpGet
from ldpy.util import httpPost
from ldpy.util import httpPut
from ldpy.util import httpDelete
from ldpy.util import triplipy
from ldpy.util import prefixesUp
from ldpy.util import parser


class Client():
    def __init__(self,endpoint,username,password):

        #Set parameters:
        self.endpoint=endpoint
        self.username=username
        self.password=password
        self.containers=dict()
        self.resources=dict()


        # Check HTTP 200:

        headers = {"accept": "text/turtle"}
        resp = httpGet(
            endpoint=self.endpoint,
            headers=headers,
            username=self.username,
            password=self.password)
        if resp:
            print("Access accepted: ")
            print(resp)
        

        # RDF parser: parse all container inside current endpoint
        # push them inside a dict {URL:Slug}

        mat = parser(resp,"container")
        self.containers.update(mat)
        
        print("Available containers at this directory:")
        for k,v in self.containers.items():
            print("Container's endpoint: ", k,"\t","Slug: ",v)

    def addNewContainer (self,slug,location):
        Container.__init__(self.endpoint,self.username,self.password,self.containers,self.resources,slug,location, method=True)
        return Container
    def setNewEndpoint(self,uri): # set new endpoint to work in a different directory
        username =self.username
        password = self.password
        return self.__init__(uri,username,password)
         

class Container(Client):
    def __init__(self, endpoint,username,password,containers,resources,method):
        
        # Set parameters:
        self.endpoint=endpoint
        self.username=username
        self.password=password
        self.containers=containers
        self.resources=resources
        self.method=method
        
        # Check HTTP 200:
        headers= {"accept": "text/turtle"}
        req = httpGet(
            endpoint=self.endpoint,
            headers=headers,
            username=self.username,
            password=self.password)

        if not req:
            sys.exit()

        # Create Container:

        if self.method:

            endpoint=""
            # Set endpoint based on previous containers' slugs
            dd= dict((k,v) for k, v in self.containers.items() if v == location)
            if len(dd) == 1:
                for dc in dd:
                    endpoint = dc
            elif len(dd) == 0:
                sys.exit("No matchable uri for the container, the container is not in the registry")
            else:
                sys.exit("Too many containers with the same name")
                
            
            # POST request to create it:
            headers={"Accept": "text/turtle", "Content-Type": "text/turtle",
                "Slug": slug ,"Link" : '<http://www.w3.org/ns/ldp#BasicContainer>; rel="type"'}

            payload="""@prefix ldp: <http://www.w3.org/ns/ldp#> . 
                        <> a ldp:Container, ldp:BasicContainer ."""
            
            resp= httpPost(url=str(endpoint),
                                headers=headers,
                                payload=payload,
                                username=self.username,
                                password=self.password)
            if not resp:
                sys.exit("Error, response from POST request: Creation of {slug} have not worked")
            else:
                print("Container named {} correctly created".format(slug))
            
            # Append this new Container to containers' dict:
            loc=resp.headers["Location"]
            self.containers.update({loc: slug})
            print("Current containers registered: ")
            for k,v in self.containers.items():
                print("Slug: ", v,"\t","Container's endpoint: ",k)
        else:
            sys.exit()

    def addMetadata_Cont(self,location,g):
    
        headers={"Accept": "text/turtle", "Content-Type": "text/turtle"}
        endpoint=""
        
        # Set endpoint based on previous containers' slugs
        dd= dict((k,v) for k, v in self.containers.items() if v == location)
        
        if len(dd) == 1:
            for dc in dd:
                endpoint = dc
        elif len(dd) == 0:
            sys.exit("No matchable uri for the container, the conatainer is not in the registry")
        else:
            sys.exit("Too many containers with the same name")
            

            
        # GET request to obtain what's inside:
        headers_get = {"Accept": "text/turtle"}
        prev_data = httpGet(
            endpoint=endpoint,
            headers=headers_get,
            username=self.username,
            password=self.password)
        
        # Depends of the input type, use triplify function or not:
        if str(type(g)) == "<class 'rdflib.graph.Graph'>":
            gg = g.serialize(format='turtle').decode("utf-8")
        elif type(g) == list: # "<class 'list'>"
            graph=Graph()
            for spo in g:
                s,p,o = spo
                triplipy(s,p,o,graph)
            gg = graph.serialize(format='turtle').decode("utf-8")
        else:
            print("Added metadata do not have correct type (list or rdflib.graph.Graph)")
        
        
        
        # PATCH response + graph to put prefix in the top of the file:
        resp_text=prev_data
        resp_text = resp_text + "\n" 
        resp_text = resp_text + str(gg)
        patch_text=prefixesUp(b = resp_text)
        
        
        # Once data curation, preforms PUT request to update metadata information:
        
        headers={"Accept": "text/turtle", "Content-Type": "text/turtle"}
        resp_put=httpPut(url=str(endpoint),
                                    headers=headers,
                                    payload=patch_text,
                                    username=self.username,
                                    password=self.password)
        if resp_put:
            print(patch_text)

    def delete(self,location):
    
        endpoint=""
        # Set endpoint based on previous containers' slugs
        dd= dict((k,v) for k, v in self.containers.items() if v == location)
        if len(dd) == 1:
            for dc in dd:
                endpoint = dc
        elif len(dd) == 0:
            sys.exit("No matchable uri for the container, the container is not in the registry")
        else:
            sys.exit("Too many containers with the same name")

        # DELETE request for this Container
        headers={"Accept":"*/*"}
        resp= httpDelete(url=str(endpoint),
                            headers=headers,
                            username=self.username,
                            password=self.password)
        if resp:
            print("The container named {} has been deleted".format(location))
        else:
            sys.exit()
        



