# -*- coding: utf-8 -*-



"""
Creates txt of all DRUG_KIND

"""


#################      DEFINITION START     ####################   

"""
Defining Proxy Server Values
(Optional)

"""

# http_proxy  = "http://username:password@proxyip:proxyport/"   
# https_proxy = "https://username:password@proxyip:proxyport/"


# proxyDict = { 
#               "http"  : http_proxy, 
#               "https" : https_proxy, 
#             }
            
            
def get_drugs():
    """
    This function pings for json objects of Drugs kind in the NDRrt database
    It then prints them on to a txt file for further use
    
    """
    kind='DRUG_KIND'
    url = 'https://rxnav.nlm.nih.gov/REST/Ndfrt/allconcepts.json?kind='+kind
    r = requests.get(url)
    #r = requests.get(url, proxies=proxyDict) #if proxy is needed
    data = r.json()
    groupConcepts = data['groupConcepts']
    target = open('drugs.txt', 'w')
    
    try:
        drugs = groupConcepts[0]['concept']
        for obj in drugs:
            del obj['conceptKind']
            target.write("%s\n" % obj)
           
        print (drugs)
        print (len(drugs))
        
    except:
        print("empty")
    target.close()    
        
 #################      DEFINITION END      ####################   

 #################      MAIN PROGRAM        ####################

import requests
        
get_drugs()

"""
list of Dict of a drugs
[
 {  1.name:
    2.nui:
    2.may_prevent:
    3.may_treat:
    4.has_MoA:
    5.has_PE:
 },
 {......
 }
]    
    
    
    
"""
