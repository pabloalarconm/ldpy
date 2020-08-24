from rdflib import Graph, Literal, RDF, URIRef
import re
import sys
import requests



class Client():
    
    def __init__(self, endpoint , username, password):

        self.endpoint=endpoint
        self.username=username
        self.password=password
        self.containers=dict()
        self.resources=dict()
        
        
        # Check if GET protocol is resolvable for this endpoint and authorization:
        headers= {"accept": "text/turtle"}
        req = Client.get(
            endpoint=self.endpoint,
            headers=headers,
            username=self.username,
            password=self.password)
        if req:
            print("Access accepted:")
            print(req)
        
        # Obtain all existing containers inside this conatiner and their slugs:
        
        mat = Client.match_containers(req,self.endpoint)
        self.containers.update(mat)
        
        print("Available containers at this directory:")
        for k,v in self.containers.items():
            print("Slug: ", v,"\t","Container's endpoint: ",k)
            
            
        # Create an Container's object:

        self.containers_level=Container(self.endpoint,
                                           self.username,
                                           self.password,
                                           self.containers,
                                           self.resources)
        # Create an Resource's object:
        
        self.resources_level=Resource(self.endpoint,
                                        self.username,
                                        self.password,
                                        self.containers,
                                        self.resources)
        
    
    
    def set_new_endpoint(self,uri): # set new endpoint to work in a different directory
        username =self.username
        password = self.password
        
        self.__init__(uri,username,password)
        
    
    
    def get(endpoint,headers,username,password):
        try:
            response=requests.get(
                url=str(endpoint),
                headers=headers,
                auth=(username,password)
            )
            return(response.text)

        except requests.ConnectionError as c:
            print("Error Connecting: ",c)
            response = False
            sys.exit()
        except requests.RequestException as e:
            print("OOps: Something Else:" ,e)
            response = False
            sys.exit()
        except requests.exceptions.Timeout as tm:
            print ("Timeout Error: ",tm)
            response = False
            sys.exit()
        except requests.exceptions.HTTPError as err:
            print("Http Error: ",err)
            response = False
            sys.exit()

            
    def delete(url,headers,username,password):
        try:
            response=requests.delete(
                url=str(url),
                headers=headers,
                auth=(username,password)
            )
            return(response)

        except requests.ConnectionError as c:
            print("Error Connecting: ",c)
            response = False
            sys.exit()
        except requests.RequestException as e:
            print("OOps: Something Else:" ,e)
            response = False
            sys.exit()
        except requests.exceptions.Timeout as tm:
            print ("Timeout Error: ",tm)
            response = False
            sys.exit()
        except requests.exceptions.HTTPError as err:
            print("Http Error: ",err)
            response = False
            sys.exit()

            

    def post(url,headers,payload,username,password):
        try:
            response=requests.post(
                url=str(url),
                headers=headers,
                data=payload,
                auth=(username,password)
            )
            return(response)

        except requests.ConnectionError as c:
            print("Error Connecting: ",c)
            response = False
            sys.exit()
        except requests.RequestException as e:
            print("OOps: Something Else: ",e)
            response = False
            sys.exit()
        except requests.exceptions.Timeout as tm:
            print ("Timeout Error: ",tm)
            response = False
            sys.exit()
        except requests.exceptions.HTTPError as err:
            print("Http Error: ",err)
            response = False
            sys.exit()

            
        
    def put(url,headers,payload,username,password):
        try:
            response=requests.put(
                url=str(url),
                headers=headers,
                data=payload,
                auth=(username,password)
            )
            return(response.text)

        except requests.ConnectionError as c:
            print("Error Connecting: ",c)
            response = False
            sys.exit()
        except requests.RequestException as e:
            print("OOps: Something Else: ",e)
            response = False
            sys.exit()
        except requests.exceptions.Timeout as tm:
            print ("Timeout Error: ",tm)
            response = False
            sys.exit()
        except requests.exceptions.HTTPError as err:
            print("Http Error: ",err)
            response = False
            sys.exit()

            

    def patch(b):

        prefixes=[]
        body=[]
        ordened=[]

        sep=b.split("\n")

        for l in sep:
            mat=re.search(r"@prefix",l)
            if mat:
                prefixes.append(l)
            else:
                body.append(l)
        for ap in prefixes:
            ordened.append(ap)
        for ap in body:
            ordened.append(ap)

        ordened_join ="\n".join(ordened)
        return(ordened_join)


    
    def triplipy(s,p,o,g):
        
        #Subject:
        s.strip()
        ss=s.split()
        m_http=re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',s)
        if str(type(s))== "<class 'rdflib.term.URIRef'>":
            pass
        elif len(ss) == 1 and m_http:
            s=URIRef(str(s))
        elif len(ss) >1 and m_http:
            sys.exit("Multiple word string cant be a Subject")
        else:
            sys.exit("Not matchable Subject")
            
        #Predicate:
        p.strip()
        pp=p.split()
        m_http=re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',p)
        if str(type(p))== "<class 'rdflib.term.URIRef'>":
            pass
        elif len(pp) == 1 and m_http:
            p=URIRef(str(p))
        elif len(pp) >1 and m_http:
            sys.exit("Multiple word string cant be a Predicate")
        else:
            sys.exit("Not matchable Predicate")
            
            
        #Object:
        m_http=re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',o)
        m_date=re.match(r"[\d]{1,2}-[\d]{1,2}-[\d]{2}",o)
        m_float=re.match(r"[-+]?\d*\.\d+|\d+",o)
        m_init=re.match(r"[+-]?[0-9]+$",o)
        oo=o.split()
        #Check if its a rdflib object:
        if str(type(o))=="<class 'rdflib.term.URIRef'>":
            pass
        #Check if its a URI:
        elif len(o) == 1 and m_http: # Check if there's more than a single URI.
            o= URIRef(str(o))
        elif len(o) > 1 and m_http:
            o = Literal(str(o),lang='en')
        elif m_date:
            o = Literal(str(o),datatype=XSD.date)
        elif m_float:
            o = Literal(str(o),datatype=XSD.float)
        elif m_init:
            o = Literal(str(o),datatype=XSD.init)
        else:
            o = Literal(str(o),lang='en')
            
        g.add([s,p,o])
        
        
    def match_containers(text,endpoint):
        
        sep=text.split("\n")
        matches=[]
        for l in sep:
                check1=re.search(r"{}".format(endpoint),l)
                if check1:
                    l_s = l.strip()
                    matches.append(l_s)
        matches2=[]
        for m in matches:
            check2=re.match(r"ldp:contains",m)
            check3=re.match(r"@prefix",m)
            if not (check2 or check3):
                matches2.append(m)           
        matches_rep=[]
        for i in matches2:
            if i not in matches_rep:
                matches_rep.append(i)
        matches_clean=[]
        for c in matches_rep:
            c=c.replace("<","").replace(">","")
            matches_clean.append(c)

        keys=matches_clean
        keys2=[]
        for k in keys:
            k=k.replace("{}".format(endpoint),"").replace("<","").replace(">","").replace("/","").replace("'","")
            keys2.append(k)

        dd=dict(zip(matches_clean, keys2))
        dd.update( {endpoint: "parent_container"} )
        ddd={}
        for k,v in dd.items():
            if not v == "":
                ddd.update({k:v})
        return(ddd)









class Container(Client):
    
    def __init__(self, endpoint,username,password,containers,resources):

        self.endpoint=endpoint
        self.username=username
        self.password=password
        self.containers=containers
        self.resources=resources
        
        headers= {"accept": "text/turtle"}
        
        req = Client.get(
            endpoint=self.endpoint,
            headers=headers,
            username=self.username,
            password=self.password)

        if not req:
            sys.exit
        
#         mat = Client.match_containers(req,self.endpoint)
#         self.containers.update(mat)
#         print(self.containers)
        
        
        self.resources_level=Resource(self.endpoint,
                                   self.username,
                                   self.password,
                                   self.containers,
                                   self.resources)
            
        

    def addnewcontainer(self,location,slug):
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
        
        resp=Client.post(url=str(endpoint),
                            headers=headers,
                            payload=payload,
                            username=self.username,
                            password=self.password)
        if not resp:
            sys.exit("Error, response from POST request: Creation of {slug} have not worked")
        else:
            print("Container named {} correctly created".format(slug))
        
        # Append this new Container to containers' dictionary:
        loc=resp.headers["Location"]
        self.containers.update({loc: slug})
        print("Current containers registered: ")
        for k,v in self.containers.items():
            print("Slug: ", v,"\t","Container's endpoint: ",k)
            


    def add_metadata_to_Cont(self,location,g):

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
        prev_data = Client.get(
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
                Client.triplipy(s,p,o,graph)
            gg = graph.serialize(format='turtle').decode("utf-8")
        else:
            print("Added metadata do not have correct type (list or rdflib.graph.Graph)")
        
        
        
        # PATCH response + graph to put prefix in the top of the file:
        resp_text=prev_data
        resp_text = resp_text + "\n" 
        resp_text = resp_text + str(gg)
        patch_text=Client.patch(b = resp_text)
        
        
        # Once data curation, preforms PUT request to update metadata information:
        
        headers={"Accept": "text/turtle", "Content-Type": "text/turtle"}
        resp_put=Client.put(url=str(endpoint),
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
        resp=Client.delete(url=str(endpoint),
                            headers=headers,
                            username=self.username,
                            password=self.password)
        if resp:
            print("The container named {} has been deleted".format(location))
        else:
            sys.exit()





class Resource(Container):
    
    def __init__(self, endpoint,username,password,containers,resources):

        self.endpoint=endpoint
        self.username=username
        self.password=password
        self.containers=containers
        self.resources=resources

            
    def addnewresource(self,location,slug,g):
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
        
        if str(type(g)) == "<class 'rdflib.graph.Graph'>":
            gg = g.serialize(format='turtle').decode("utf-8")
        elif type(g) == list: # "<class 'list'>"
            graph=Graph()
            for spo in g:
                s,p,o = spo
                Client.triplipy(s,p,o,graph)
            gg = graph.serialize(format='turtle').decode("utf-8")
        else:
            print("Added metadata do not have correct type (list or rdflib.graph.Graph)")
            
            
        headers = {"Accept":"text/turtle","Content-Type": "text/turtle",
                   "Slug" : slug,
                   "Link" : '<http://www.w3.org/ns/ldp#Resource>; rel="type"'}
        
        payload = """<> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/ldp#Resource> ."""

        
        
        payload = payload + "\n" 
        payload = payload + str(gg)
        patch_text=Client.patch(b = payload)
        
        resp=Client.post(url=str(endpoint),
                            headers=headers,
                            payload=patch_text,
                            username=self.username,
                            password=self.password)
        if not resp:
            sys.exit("Error, response from POST request: Creation of {slug} have not worked")
        else:
            print("Resource named {} correctly created".format(slug))
            
        
        # Append this new Container to containers' dictionary:
        loc=resp.headers["Location"]
        self.resources.update({loc: slug})
        for k,v in self.resources.items():
            print("Slug: ", v,"\t","Resource's endpoint: ",k)


    def add_metadata_to_Res(self,location,g):

        headers={"Accept": "text/turtle", "Content-Type": "text/turtle"}
        endpoint=""
        
        # Set endpoint based on previous resources' slugs
        dd= dict((k,v) for k, v in self.resources.items() if v == location)
        
        if len(dd) == 1:
            for dc in dd:
                endpoint = dc
        elif len(dd) == 0:
            sys.exit("No matchable uri for the container, the conatainer is not in the registry")
        else:
            sys.exit("Too many containers with the same name")
            

            
        # GET request to obtain what there's inside:
        headers_get = {"Accept": "text/turtle"}
        prev_data = Client.get(
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
                Client.triplipy(s,p,o,graph)
            gg = graph.serialize(format='turtle').decode("utf-8")
        else:
            print("Added metadata do not have correct type (list or rdflib.graph.Graph)")
        
        
        
        # PATCH response + graph to put prefix in the top of the file:
        resp_text=prev_data
        resp_text = resp_text + "\n" 
        resp_text = resp_text + str(gg)
        patch_text=Client.patch(b = resp_text)
        
        # Once data curation, preforms PUT request to update metadata information:
        
        headers={"Accept": "text/turtle", "Content-Type": "text/turtle"}
        resp_put=Client.put(url=str(endpoint),
                                    headers=headers,
                                    payload=patch_text,
                                    username=self.username,
                                    password=self.password)
        if resp_put:
            print(patch_text)
        
    def delete(self,location):

        endpoint=""
        # Set endpoint based on previous containers' slugs
        dd= dict((k,v) for k, v in self.resources.items() if v == location)
        if len(dd) == 1:
            for dc in dd:
                endpoint = dc
        elif len(dd) == 0:
            sys.exit("No matchable uri for the container, the container is not in the registry")
        else:
            sys.exit("Too many containers with the same name")

        # DELETE request for this Container
        headers={"Accept":"*/*"}
        resp=Client.delete(url=str(endpoint),
                                headers=headers,
                                username=self.username,
                                password=self.password)
        if resp:
            print("The resource named {} has been deleted".format(location))
        else:
            sys.exit()

            