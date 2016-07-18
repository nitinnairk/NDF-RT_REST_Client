# -*- coding: utf-8 -*-
"""
Created on Fri May 27 19:00:31 2016

@author: nitin
"""

import threading
import Queue
import sys
import ast
import requests




def api_call(url):

    """

    This function requests data from  'url' and stores the required info in 'ans'
    
    """

    ans=[]
    r = requests.get(url)
    #r = requests.get(url, proxies=proxyDict) #if proxy needed
    data = r.json()
    groupConcepts = data['groupConcepts']
    try:
        concepts=groupConcepts[0]['concept']
    except:
        return None
    
    for obj in concepts:
        print obj['conceptName']
        ans.append(obj['conceptName'])
    return ans



def do_work(in_queue):
    """

    Here the queue which contains dict type obj is read whose NUI which is a unique ID for each unique drug is first read and json data is then requested
    for all the roles mentioned in 'diff_rel' of the NUI read.
    This data is then added with the key role on to the dict type obj 'dict_obj' and this is then appended to the txt file 'drugs_data.txt' 
    

    Def:
    diff_rel        : List of all the 'rolename' which needs to be extracted.
    drugs_data.txt  : txt file which contains the dict type obj which is retuned from api_call() and the queued dict.

    RESTful call used: /role
    Get the related concepts by role. In NDF-RT, the relations between two concepts are defined by roles and are one directional. 
    For example, "Fenofibrate" "may_treat" "Arteriosclerosis" is an example of a relationship in NDF-RT where the 
    role "may_treat" is the relationship between the drug "Fenofibrate" (the subject) and the disease "Arteriosclerosis"(the object).
    To determine which diseases the drug "Fenofibrate" "may_treat", this resource specifies the subject and the role.

    For more information visit the link below
    source: https://mor.nlm.nih.gov/download/rxnav/NdfrtAPIREST.html#uLink=Ndfrt_REST_getRelatedConceptsByRole






    """
    diff_rel=['may_treat','may_prevent','has_MoA','has_PE']
    while True:
	flag = False
        dict_obj = in_queue.get()
        
        print dict_obj["conceptNui"]
        
        for role in diff_rel:
            data_role=[]  
            url = 'https://rxnav.nlm.nih.gov/REST/Ndfrt/role.json?nui=' + dict_obj["conceptNui"] +  '&roleName='  +   role  +   '%20{NDFRT}&transitive=false'
            data_role=api_call(url)
            if data_role is not None:
              dict_obj[role] = data_role  
              flag=True
        if flag is True:
            lock_th.acquire()
            target = open('drugs_data.txt', 'a')
            target.write("%s\n" % dict_obj)
            target.close()
	    lock_th.release()
            flag = False
            
        in_queue.task_done()

if __name__ == "__main__":
    """
    
    Here drugs.txt is read which was created using 'get_drugs.py'
    These dict type objs are then put into a queue 'work' this is then passed onto the do_work() function.

    Proxy def is optional.

    Multithreading is used to reduce the time taken for data retrieval substaintially.

    Def:
    work    : Queue which contains dict ype obj from drugs.txt
    lock_th : Used for locking the txt file in do_work() to prevent write conflicts

    """
    work = Queue.Queue()
    
    lock_th=threading.Lock()
    
    
    #http_proxy  = "http://username:password@proxyip:proxyport/"   
    #https_proxy = "https://username:password@proxyip:proxyport/"


    #proxyDict = { 
    #          "http"  : http_proxy, 
    #          "https" : https_proxy, 
    #             }



    # start for workers
    workers_no = 100
    for i in xrange(workers_no):
        t = threading.Thread(target=do_work, args=(work,))
        t.daemon = True
        t.start()
    
    read_tar = open('drugs.txt','r')
    for obj in read_tar:
        dict_obj = ast.literal_eval(obj)
        work.put(dict_obj)
        
    read_tar.close()
    
    work.join()
    sys.exit()
