import os
import json
import random
import random
from math import *
from utilities import *
#just shit!

ROTATE_LEFT = "rotate-left"
ROTATE_RIGHT = "rotate-right"
ADVANCE = "advance"
RETREAT = "retreat"
SHOOT = "shoot"
PASS = "pass"

MOVE_UP =  {"top" : ADVANCE, "bottom" : ROTATE_LEFT, "right" : ROTATE_LEFT ,"left" : ROTATE_RIGHT }
MOVE_DOWN =  {"top" : ROTATE_LEFT, "bottom" : ADVANCE, "right" : ROTATE_RIGHT ,"left" : ROTATE_LEFT }
MOVE_RIGHT = {"top" : ROTATE_RIGHT, "bottom" : ROTATE_LEFT, "right" : ADVANCE ,"left" : ROTATE_LEFT }
MOVE_LEFT = {"top" : ROTATE_LEFT, "bottom" : ROTATE_RIGHT, "right" : ROTATE_RIGHT,"left" : ADVANCE }

def chooseAction(body):
    action = PASS

    powerX, powerY = findClosestPower(body)
    upX, upY = closestPowerup(body)


    posX = random.randint(0, body["mapWidth"])
    posY = random.randint(0, body["mapHeight"])


    if powerX != -1:
        action = moveTowardsPoint(body, powerX, powerY)
    elif upX != -1:
        try:
            action = moveTowardsPoint(body, body["enemies"][0]["x"], body["enemies"][0]["y"])
        except:
            action = moveTowardsPoint(body, upX, upY)

    else:
        action = moveTowardsPoint(body, posX, posY)
    if shootIfPossible(body):
        action = SHOOT
    return action



env = os.environ
req_params_query = env['REQ_PARAMS_QUERY']
responseBody = open(env['res'], 'w')

response = {}
returnObject = {}
if req_params_query == "info":
    returnObject["name"] = "HunterXHunter"
    returnObject["team"] = "Charming python"
elif req_params_query == "command":    
    body = json.loads(open(env["req"], "r").read())
    returnObject["command"] = chooseAction(body)

response["body"] = returnObject
responseBody.write(json.dumps(response))
responseBody.close()