import json

keystore=set([112233,456789,785634]) #contains secret keys of all the users.


def lambda_handler(event, context):
    print(event)
    inp=event["queryStringParameters"]
    key=inp["send_secret"]

    if int(key) not in keystore:
        return  {
        'statusCode': 200,
        'body': json.dumps("authentication error")
        }

    out={}
    out["result_status"]=0
    if inp["device"]=="bulb":
        if int(inp["action"])==0:
            out["result_state"]=0
        elif int(inp["action"])==1:
            out["result_state"]=float(inp["curr_state"])
        elif int(inp["action"])==2:
            out["result_state"]=min(float(inp["curr_state"])+25,100)
        elif int(inp["action"])==3:
            out["result_state"]=max(float(inp["curr_state"])-25,0)
        out["id"]=int(inp["id"])
        
        
        
        
        
        
    elif inp["device"]=="fan":
        if int(inp["action"])==0:
            out["result_state"]=0
        elif int(inp["action"])==1:
            out["result_state"]=float(inp["curr_state"])
        elif int(inp["action"])==2:
            out["result_state"]=min(float(inp["curr_state"])+25,100)
        elif int(inp["action"])==3:
            out["result_state"]=max(float(inp["curr_state"])-25,0)
        out["id"]=int(inp["id"])
    elif inp["device"]=="ac":
        if int(inp["action"])==0:
            out["result_state"]=0
        elif int(inp["action"])==1:
            out["result_state"]=float(inp["curr_state"])
        elif int(inp["action"])==2:
            out["result_state"]=min(float(inp["curr_state"])+25,100)
        elif int(inp["action"])==3:
            out["result_state"]=max(float(inp["curr_state"])-25,0)
        out["id"]=int(inp["id"])
    else :
        if int(inp["action"])==0:
            out["result_state"]=0
        elif int(inp["action"])==1:
            out["result_state"]=float(inp["curr_state"])
        elif int(inp["action"])==2:
            out["result_state"]=min(float(inp["curr_state"])+25,100)
        elif int(inp["action"])==3:
            out["result_state"]=max(float(inp["curr_state"])-25,0)
        out["id"]=int(inp["id"])
    out["result_status"]=1
    return {
        'statusCode': 200,
        'body': json.dumps(out)
        }
    