from rdflib import Graph, Literal, RDF, URIRef
import re
import sys
import requests

from ldpy.util import httpGet, httpPost, httpPut, httpDelete
from ldpy.util import triplipy, prefixesUp, parser



class Client(object):

    def __init__(self,endpoint,username,password): # Set conexion to LDP Server and parse metadata from the endpoint:

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
        # Push them into dict {URL:Slug}
        mat = parser(resp,"container")
        self.containers.update(mat)
        mat2 = parser(resp,"resource")
        self.resources.update(mat2)

        # Show parser results:
        print("Available containers at this directory:")
        for k,v in self.containers.items():
            print("Container's endpoint: ", k,"\t","Slug: ",v)
        print("Available resources at this directory:")
        for k,v in self.resources.items():
            print("Resource's endpoint: ", k,"\t","Slug: ",v)

    def addNewContainer (self,location,slug): # Creates a new object with class Container
        conti=Container(self.endpoint,self.username,self.password,self.containers,self.resources,location, method = True, slug=slug)
        return conti

    def SetCurrentContainer (self,location): # Set certain repo as current Container object to work from it
        conti=Container(self.endpoint,self.username,self.password,self.containers,self.resources,location,method=False)
        return conti

    def setNewEndpoint(self,endpoint): # Set new endpoint to work in a different directory
        Client.__init__(self,endpoint,self.username,self.password)
        return Client

    def addNewResource (self,slug,g,location): # Creates a new object with class Resource
        res=Resource(self.endpoint,self.username,self.password,self.containers,self.resources,location, method = True, slug=slug, g=g)
        return res 

    def SetCurrentResource (self,location):# Set certain repo as current Resource object to work from it
        res=Resource(self.endpoint,self.username,self.password,self.containers,self.resources,location, method = False)
        return res

class Container(object):

    def __init__(self,endpoint,username,password,containers,resources,location, method,**kwargs):

        # Set parameters
        self.endpoint=endpoint
        self.username=username
        self.password=password
        self.containers=containers
        self.resources=resources
        self.location=location

        #Set optional parameters:
        slug =""
        for k,v in kwargs.items():
            if k == "slug":
                slug = v
        
        # Check HTTP GET:
        headers= {"accept": "text/turtle"}
        req = httpGet(
            endpoint=self.endpoint,
            headers=headers,
            username=self.username,
            password=self.password)
        if not req:
            sys.exit()

        # Before Creating/moving to this Container, a new RDF parser will be called to check all Containers and Resources from new endpoint and added to dict()
        mat = parser(req,"container")
        self.containers.update(mat)
        mat2 = parser(req,"resource")
        self.resources.update(mat2)
        
        # Find endpoint based on dict based on Slug's endpoint:
        dd = dict((k,v) for k, v in self.containers.items() if v == self.location)

        if len(dd) == 1:
            for k,v in dd.items():
                self.endpoint = k
        elif len(dd) == 0:
            sys.exit("No matchable uri for the container, the container is not in the registry")
        else:
            sys.exit("Too many containers with the same name") # TO-DO: Add prompt form to choose between endpoints

        if method:
            # HTTP POST to create Container
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
            
            # Append this new container to containers' dict:
            loc=resp.headers["Location"]
            self.containers.update({loc: slug})
            print("Current containers registered: ")
            for k,v in self.containers.items():
                print("Container's endpoint: ",k,"\t","Slug: ", v)
            # Set new endpoint to work from it
            self.endpoint=loc
        elif method==False:
            print("Now your working at: {} as a container".format(self.endpoint))
        else:
            sys.exit()
    
    def addMetadataCont(self,g): # HTTP PUT prev + graph to Resource's metadata:

        # HTTP GET:
        headers_get = {"Accept": "text/turtle"}

        prev_data = httpGet(
            endpoint=self.endpoint,
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

        # PATCH response + graph and put prefix in the top of the file:
        resp_text=prev_data
        resp_text = resp_text + "\n" 
        resp_text = resp_text + str(gg)
        patch_text=prefixesUp(b = resp_text)
        
        # Once data curation, HTTP PUT to update metadata information:
        headers={"Accept": "text/turtle", "Content-Type": "text/turtle"}
        resp_put=httpPut(url=str(self.endpoint),
                                    headers=headers,
                                    payload=patch_text,
                                    username=self.username,
                                    password=self.password)
        if resp_put:
            print(patch_text)

    def delete(self):# HTTP DELETE for this Container:

        headers={"Accept":"*/*"}
        resp= httpDelete(url=str(self.endpoint),
                            headers=headers,
                            username=self.username,
                            password=self.password)
        if resp:
            print("The container named {} has been deleted".format(self.endpoint))
        else:
            sys.exit()
        
    def get(self): # HTTP GET of this Container:
        
        headers= {"accept": "text/turtle"}
        req = httpGet(
            endpoint=self.endpoint,
            headers=headers,
            username=self.username,
            password=self.password)

        print(req)

        if not req:
            sys.exit()

    def addNewResource (self,slug,g,location): # Creates a new object with class Resource
        res=Resource(self.endpoint,self.username,self.password,self.containers,self.resources,location, method = True, slug=slug, g=g)
        return res

    def SetCurrentResource (self,location):# Set certain repo as current Resource object to work from it
        res=Resource(self.endpoint,self.username,self.password,self.containers,self.resources,location, method = False)
        return res 

    def addNewContainer (self,location,slug): # Creates a new object with class Container
        conti=Container(self.endpoint,self.username,self.password,self.containers,self.resources,location, method = True, slug=slug)
        return conti

    def SetCurrentContainer (self,location): # Set certain repo as current Container object to work from it
        conti=Container(self.endpoint,self.username,self.password,self.containers,self.resources,location,method=False)
        return conti

class Resource(object):
    
    def __init__(self,endpoint,username,password,containers,resources,location, method, **kwargs):

        # Set parameters
        self.endpoint=endpoint
        self.username=username
        self.password=password
        self.containers=containers
        self.resources=resources
        self.location=location

        #Set optional parameters:
        slug = ""
        g = ""
        for k,v in kwargs.items():
            if k == "slug":
                slug = v
            if k == "g":
                g = v

        # Check HTTP GET:
        headers= {"accept": "text/turtle"}
        req = httpGet(
            endpoint=self.endpoint,
            headers=headers,
            username=self.username,
            password=self.password)
        if not req:
            sys.exit()

        # Before Creating/moving to this Container, a new RDF parser will be called to check all Containers and Resources from new endpoint and added to dict()
        mat = parser(req,"container")
        self.containers.update(mat)
        mat2 = parser(req,"resource")
        self.resources.update(mat2)
        
        # Find endpoint based on dict based on Slug's endpoint:
        if method == True:
            dd = dict((k,v) for k, v in self.containers.items() if v == self.location)
        elif method == False:
            dd = dict((k,v) for k, v in self.resources.items() if v == self.location)
        else:
            sys.exit()

        if len(dd) == 1:
            for k,v in dd.items():
                self.endpoint = k
        elif len(dd) == 0:
            sys.exit("No matchable uri for the container, the container is not in the registry")
        else:
            sys.exit("Too many containers with the same name") # TODO: Add prompt form to choose between endpoints

        if method: 
            # Create Resource and add metadata on it
            # Resource's metadata sanity check:
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
                
            # Basic info by default:    
            headers = {"Accept":"text/turtle","Content-Type": "text/turtle",
                    "Slug" : slug,
                    "Link" : '<http://www.w3.org/ns/ldp#Resource>; rel="type"'}
            
            payload = """<> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/ldp#Resource> ."""

            
            # Patch data in order to have all prefixes up:
            payload = payload + "\n" 
            payload = payload + str(gg)
            patch_text= prefixesUp(b = payload)
            
            resp= httpPost(url=str(endpoint),
                                headers=headers,
                                payload=patch_text,
                                username=self.username,
                                password=self.password)
            if not resp:
                sys.exit("Error, response from POST request: Creation of {slug} have not worked")
            else:
                print("Resource named {} correctly created".format(slug))
                
            
            # Append this new resource to resources' dictionary:
            loc=resp.headers["Location"]
            self.resources.update({loc: slug})
            for k,v in self.resources.items():
                print("Resource's endpoint: ",k,"\t","Slug: ", v)
            # Set new endpoint to work from it
            self.endpoint= loc
        elif method==False:
            print("Now your working at: {} as a resource".format(self.endpoint))
        else:
            sys.exit()

    def addMetadataRes(self,g): # HTTP PUT prev + graph to Resource's metadata:
    
        # HTTP GET:
        headers_get = {"Accept": "text/turtle"}

        prev_data = httpGet(
            endpoint=self.endpoint,
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

        # PATCH response + graph and put prefix in the top of the file:
        resp_text=prev_data
        resp_text = resp_text + "\n" 
        resp_text = resp_text + str(gg)
        patch_text=prefixesUp(b = resp_text)
        
        # Once data curation, HTTP PUT to update metadata information:
        headers={"Accept": "text/turtle", "Content-Type": "text/turtle"}
        resp_put=httpPut(url=str(self.endpoint),
                                    headers=headers,
                                    payload=patch_text,
                                    username=self.username,
                                    password=self.password)
        if resp_put:
            print(patch_text)

    def delete(self): # HTTP DELETE for this Resource

        headers={"Accept":"*/*"}
        resp= httpDelete(url=str(self.endpoint),
                            headers=headers,
                            username=self.username,
                            password=self.password)
        if resp:
            print("The container named {} has been deleted".format(self.endpoint))
        else:
            sys.exit()

    def get(self): # HTTP GET of this Resource

        headers= {"accept": "text/turtle"}
        req = httpGet(
            endpoint=self.endpoint,
            headers=headers,
            username=self.username,
            password=self.password)

        print(req)

        if not req:
            sys.exit()

