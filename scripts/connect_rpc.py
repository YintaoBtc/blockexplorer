import json, requests

#Function for connect with rpc
def instruct_wallet(method, params):

    rpc_user='bitcoinrpc'
    rpc_password='elcaminodeltao'

    
    url = "http://127.0.0.1:18332/"
    payload = json.dumps({"method": method, "params": params})
    headers = {'content-type': "application/json", 'cache-control': "no-cache"}
    try:
        response = requests.request("POST", url, data=payload, headers=headers, auth=(rpc_user, rpc_password))
        result = json.loads(response.text)
        return result
    except requests.exceptions.RequestException as e:
        print (e)
    except:
        print ('No response from Wallet, check Crown is running on this machine')