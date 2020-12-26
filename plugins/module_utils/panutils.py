DOCUMENTATION = '''
---
module: panutils
short_description: Panos utility functions
'''
import requests, json, urllib3, xmltodict, logging

def Dag_pull_all(addresses, firewall, api, dag): 
    """ Pulling all IPs registered with any tag on firewall 
        Returns IP registered with specific tag
    """
    cmd, response, tag2ip ="<show><object><registered-ip><all/></registered-ip></object></show>", {'register':[],'deregister':[]}, {dag:[]}

    url_panos = "https://" + firewall+ "/api?type=op&cmd=" + cmd+ "&key=" + api
    r = requests.get(url_panos, verify=False)
    if r.status_code == 200:
        doc = json.loads(json.dumps(xmltodict.parse(r.text)))
        entries = doc['response']['result']['entry']
        for entry in entries:
            if dag in entry['tag']['member']:
                tag2ip[dag].append(entry['@ip'])  
        response['register'].extend(Diff(addresses, tag2ip[dag]))  
        response['deregister'].extend(Diff(tag2ip[dag], addresses))
    return response

def Diff(li1, li2): 
    li_dif = [i for i in li1 if i not in li2] 
    return li_dif 

def Dag_pull(address, firewall, api, dag):    
    """ Pulling tags IP is registered with on firewall
        Return False if IP is not registered on firewall with speficic tag (or any tag at all)
    """
    cmd, response="<show><object><registered-ip><ip>" + address + "</ip></registered-ip></object></show>", None
    """
    <response status="success">
    <result>
        <entry ip="10.1.129.5" from_agent="0" persistent="1">
            <tag>
                <member>azure.vnet-name.Vnet-WestUS-Prod-Core</member>
                <member>azure.region.westus</member>
            </tag>
        </entry>
        <count>1</count>
        </result>
    </response>
    """
    url_panos = "https://" + firewall + "/api?type=op&cmd=" + cmd + "&key=" + api
    r = requests.get(url_panos, verify=False)
    if r.status_code == 200:
        doc = json.loads(json.dumps(xmltodict.parse(r.text)))
        if 'entry' not in doc['response']['result']: 
            return False 
        else:       
            member = doc['response']['result']['entry']['tag']
            if dag in member['member']:
                response = True
            else:
                response = False  
    else:
        response = False
    return response 