#!/usr/bin/python3
DOCUMENTATION = '''
---
module: panos_tags
short_description: Register IP addresses to Palo dynamic address group
'''

EXAMPLES = '''
- name: Register addresses in Panos
  panos_tags:
    url: 10.10.10.1,10.10.10.2
    dag: azure.tag
    addrlist: [1.1.1.1,2.2.2.2]
    api: ***
'''
from ansible.module_utils.basic import *
import requests, json, urllib3
from ansible.module_utils.panutils import Dag_pull, Dag_pull_all

def dag_push(addresses, firewall, provider):
    """ Registering addresses matching Azure tag to firewall """    
    cmd, errors = "", {} 
    
    headers = { 'Content-Transfer-Encoding': 'application/x-www-form-urlencoded', 'Content-Type':'application/x-www-form-urlencoded' }
    
    toReOrUnreOnFw = Dag_pull_all(addresses, firewall, provider['api'], provider['dag'])
    for register in toReOrUnreOnFw['register']:
        cmd+="""<register><entry ip="{address}" persistent="{dag_persistent}"><tag><member timeout="{dag_timeout}">{dag_tag}</member></tag></entry></register>""".format(address=str(register),dag_persistent=str(provider['persistent']), dag_timeout=str(provider['timeout']), dag_tag=str(provider['dag']))
    for deregister in toReOrUnreOnFw['deregister']:
        cmd+="""<unregister><entry ip="{address}" persistent="{dag_persistent}"><tag><member timeout="{dag_timeout}">{dag_tag}</member></tag></entry></unregister>""".format(address=str(deregister),dag_persistent=str(provider['persistent']), dag_timeout=str(provider['timeout']), dag_tag=str(provider['dag']))
    dag_cmd="""<uid-message><type>update</type><payload>{cmd}</payload></uid-message>""".format(cmd=str(cmd))
    dag_cmd=" ".join(dag_cmd.split()) # .replace(" ","")
    url_panos = "https://" + firewall + "/api?type=user-id&cmd=" + dag_cmd + "&key=" + provider['api'] # .replace(" ","")
    debug_msg, change = {}, False
    if toReOrUnreOnFw['register'] or toReOrUnreOnFw['deregister']:
        debug_msg[firewall]= url_panos.partition("&key=")[0]
        try:
            response = requests.post(url_panos, headers=headers, data = {}, verify=False)
        except requests.exceptions.RequestException as e:   
            errors[firewall] = str(e)
            return json.dumps(errors), toReOrUnreOnFw, change, debug_msg
        if response.status_code != 200:         
            errors[firewall]=response.content.decode('utf-8')
        else:
            change = True     
    return  json.dumps(errors), toReOrUnreOnFw, change, debug_msg

def main():
    fields = {
        "dag": {"required": True, "type": "str"},
        "url": {"required": True, "type": "str"},
        "api": {"required": True, "type": "str"},
        "addrlist": {"required": True, "type": "list"},
        "timeout": {"required": False, "type": "str", "default": "0"},
        "persistent": {"required": False, "type": "str", "default": "1"},
    }    

    module = AnsibleModule(argument_spec=fields)
    tag = module.params['dag']
    url = module.params['url']
    api = module.params['api']
    addrlist = [str(addr).strip() for addr in module.params['addrlist']]
    timeout = module.params['timeout']
    persistent = module.params['persistent']
    provider = {
        "dag": str(tag),
        "url": str(url),
        "api": str(api),
        "addrlist": addrlist,
        "timeout": str(timeout),
        "persistent": str(persistent)
        }
    module.log(msg="Fields: {}".format(json.dumps(provider)))     
    firewalls = list(url.split(","))   
    debug_msg = "Firewalls:"
    if addrlist:
        for firewall in firewalls:
            module.log("Firewall: {}".format(firewall)) 
            debug_msg= debug_msg + "{} ".format(firewall.strip())
            errors, toDoOnFw, change, msg = dag_push(addrlist, firewall.strip(), provider)
            module.log("(dag_push) -> errors: {} result {}".format(errors, toDoOnFw))  
        if bool(errors):
            module.exit_json(changed=change, meta=toDoOnFw, debug_msg=json.dumps(msg)) # debug_msg.strip() or json.dumps(msg)
        else:
            module.fail_json(msg=msg, meta=errros)
    else:
        module.exit_json(changed=False, meta={}, debug_msg="addrlist is empty")
            

if __name__ == '__main__':
    main()