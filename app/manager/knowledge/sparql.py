from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions

ENDPOINT_SPARQL = "http://127.0.0.1:3030/neo/sparql"
ENDPOINT_UPDATE = "http://127.0.0.1:3030/neo/update"

def _class_prop_fetch():
    sparql = SPARQLWrapper(ENDPOINT_SPARQL)
    ALL_CLASSES = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT distinct ?subject ?predicate
    WHERE 
    {?subject ?predicate rdfs:Class}
    LIMIT 10
    """
    query = ALL_CLASSES
    class_list = []
    print(query)
    sparql.setQuery(query)
    sparql.method = 'POST'
    sparql.setReturnFormat(JSON)
    sparqlresults = sparql.query().convert()

    if sparqlresults["results"]["bindings"]:
        print(sparqlresults["results"]["bindings"])
        for cls in sparqlresults["results"]["bindings"]:
            # s = aclass["subject"]["value"].split('/')[-1]
            s = cls["subject"]["value"]
            ns = '<%s>' % s
            # print(s)
            # class_list.append(aklass)
            CLASS_PROPERTIES = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT DISTINCT ?o
                WHERE {
                    %s rdfs:label ?o.
            }"""
            sub_query = CLASS_PROPERTIES % (ns)
            sparql.setQuery(sub_query)
            sparql.setReturnFormat(JSON)
            sub_sparqlresults = sparql.query().convert()
            if sub_sparqlresults["results"]["bindings"]:
                for prop in sub_sparqlresults["results"]["bindings"]:
                    # p = prop["property"]["value"]
                    o = prop["o"]["value"]
                    class_list.append({'s':s, 'o':o})
    return class_list


def _class_label_comment_fetch():
    from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
    from urllib import error

    sparql = SPARQLWrapper(ENDPOINT_SPARQL)
    CLASS_LABEL_COMMENT = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT distinct ?s ?label ?comment
    WHERE 
    {
      ?s rdfs:label  ?label. 
      ?s rdfs:comment  ?comment.
    }
    """
    query = CLASS_LABEL_COMMENT
    rs_list = []
    print(query)
    sparql.setQuery(query)
    sparql.method = 'POST'
    sparql.setReturnFormat(JSON)
    sparqlresults = sparql.query().convert()
    print('sparqlresults:%s' % sparqlresults)

    if sparqlresults["results"]["bindings"]:
        # print(sparqlresults["results"]["bindings"])
        for rs in sparqlresults["results"]["bindings"]:
            # s = rs["s"]["value"].split('/')[-1]
            s = rs["s"]["value"]
            l = rs["label"]["value"]
            c = rs["comment"]["value"]
            # print(s, l, c)
            rs_list.append({'s':s, 'l':l, 'c':c})
    return rs_list

def update_aurl_properties(aURI, properties):
    from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
    from urllib import error
    messages = []

    sparql = SPARQLWrapper(ENDPOINT_UPDATE)
    query = """
    PREFIX dc: <http://purl.org/dc/elements/1.1/> 
    """

    del_duery = "DELETE { "
    ins_query = "INSERT { "
    whe_query = "WHERE { "

    if aURI and properties:
        del_duery += "%s " % (aURI)
        ins_query += "%s " % (aURI)
        for po in properties:
            del_duery += "%s ?o ; " % (po[0])
            ins_query += "%s %s ; " % (po[0], po[1])

        del_duery += " . } "
        ins_query += " . } "
        whe_query += " %s ?p ?o . }" % (aURI)
        query += del_duery + ins_query + whe_query

    else:
        messages.append('Error, Insert proper aURI and(or) predict, object fairs')
        return False, messages

    print('query:%s' % query)
    sparql.setQuery(query)
    sparql.method = 'POST'
    sparql.setReturnFormat(JSON)
    sparqlresults = None
    try:
        sparqlresults = sparql.query().convert()
        print('sparqlresults:%s' % sparqlresults)

    except error.HTTPError as e:
        print('HTTPError: %s' % e)
        messages.append(str(e))
    except SPARQLExceptions.EndPointInternalError as e:
        print('EndPointInternalError: %s' % e)
        messages.append(str(e))
    except SPARQLExceptions.QueryBadFormed as e:
        print('QueryBadFormed: %s' % e)
        messages.append(str(e))
    except Exception as e:
        print('Exception: %s' % e)
        messages.append(str(e))

    rs_idx = str(sparqlresults).find('Update succeeded')
    if rs_idx == -1:
        print('Fail, not exist')
        messages.append('Fail, not exist')
        return False, messages
    else:
        print('Success')
        messages.append('Success')
        return True, messages


def insert_aurl_properties(aURI, properties):
    from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
    from urllib import error
    messages = []

    sparql = SPARQLWrapper(ENDPOINT_UPDATE)
    query = """
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    INSERT DATA { """
    if aURI and properties:
        query += "%s " % aURI
        for po in properties:
            query += " %s %s ; " % (po[0], po[1])

        query += """
        .
        }
        """
    else:
        messages.append('Error, Insert wants proper aURI and(or) predict, object')
        return False, messages

    print('query:%s' % query)
    sparql.setQuery(query)
    sparql.method = 'POST'
    sparql.setReturnFormat(JSON)
    sparqlresults = None
    try:
        sparqlresults = sparql.query().convert()
        print('sparqlresults:%s' % sparqlresults)

    except error.HTTPError as e:
        print('HTTPError: %s' % e)
        messages.append(str(e))

    except SPARQLExceptions.EndPointInternalError as e:
        print('EndPointInternalError: %s' % e)
        messages.append(str(e))

    except SPARQLExceptions.QueryBadFormed as e:
        print('QueryBadFormed: %s' % e)
        messages.append(str(e))

    except Exception as e:
        print('Exception: %s' % e)
        messages.append(str(e))


    rs_idx = str(sparqlresults).find('Update succeeded')
    if rs_idx == -1:
        print('Fail')
        messages.append('Fail')
        return False, messages
    else:
        print('Success')
        messages.append('Success')
        return True, messages


def delete_aurl_properties(aURI, properties):
    from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
    from urllib import error
    messages = []

    sparql = SPARQLWrapper(ENDPOINT_UPDATE)
    query = """
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    DELETE { """
    if aURI and properties:
        query += "%s " % aURI
        for po in properties:
            query += " %s %s ; " % (po[0], po[1])

        query += """
        .
        }
        """
        query += " WHERE { %s ?p ?o . }" % (aURI)
    else:
        messages.append('Error, Delete wants proper aURI and(or) predict, object')
        return False, messages

    print('query:%s' % query)
    sparql.setQuery(query)
    sparql.method = 'POST'
    sparql.setReturnFormat(JSON)
    sparqlresults = None
    try:
        sparqlresults = sparql.query().convert()
        print('sparqlresults:%s' % sparqlresults)

    except error.HTTPError as e:
        print('HTTPError: %s' % e)
        messages.append(str(e))

    except SPARQLExceptions.EndPointInternalError as e:
        print('EndPointInternalError: %s' % e)
        messages.append(str(e))

    except SPARQLExceptions.QueryBadFormed as e:
        print('QueryBadFormed: %s' % e)
        messages.append(str(e))

    except Exception as e:
        print('Exception: %s' % e)
        messages.append(str(e))

    rs_idx = str(sparqlresults).find('Update succeeded')
    if rs_idx == -1:
        print('Fail')
        messages.append('Fail')
        return False, messages
    else:
        print('Success')
        messages.append('Success')
        return True, messages


if __name__ == "__main__":
    aURI = '<http://example/book3>'
    # properties = [('dc:title', "'A new book 000000'"), ('dc:creator', "'A.N.0000000'")]
    # properties = [('dc:title', "'A new book 000000'"), ('dc:creator', "'A.N.0000000'")]
    # insert_aurl_properties(aURI, properties)
    # update_aurl_properties(aURI, properties)
    # delete_aurl_properties(aURI, properties)

    #
    properties = [("?p", "?o")]
    delete_aurl_properties(aURI, properties)


