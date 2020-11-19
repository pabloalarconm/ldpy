import requests
from rdflib import Graph, URIRef , Literal
import sys
import re

## Basic HTTP protocols for Linked Data and RDF utils:

def httpGet(endpoint,headers,username,password):
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

            
def httpDelete(url,headers,username,password):
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

        

def httpPost(url,headers,payload,username,password):
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

        
    
def httpPut(url,headers,payload,username,password):
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


    def parser(response, output):
        if output == "container":
            graph=Graph()
            graph.parse(data=response, format="ttl")

            list_url=[]
            for subj, pred, obj in graph:
                if str(obj) == "http://www.w3.org/ns/ldp#Container":
                    list_url.append(str(subj))

            list_names=[]
            for l in list_url:
                wordI = l[::-1]
                wordI= wordI[1:]
                wordI = wordI.split('/')[0]
                wordI = wordI[::-1]
                list_names.append(wordI)

            dd=dict(zip(list_url,list_names))
            #dd.update( {"checking": "LDP"} )
            return(dd)
        elif output == "resource":
            print("in process")
        else:
            sys.exit()



## Before HTTP Put, make sure all prefixes are in the top of the RDF file.


def prefixesUp(b):
    
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

## Serializer:

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
        elif len(oo) == 1 and m_http: # Check if there's more than a single URI.
            o= URIRef(str(o))
        elif len(oo) > 1 and m_http:
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