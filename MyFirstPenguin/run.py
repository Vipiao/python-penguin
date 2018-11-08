import os
import json
import random
import math
import random
from math import *
#newer-est-est shit!

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

def doesCellContainWall(walls, x, y):
    for wall in walls:
        if wall["x"] == x and wall["y"] == y:
            return True
    return False

def wallInFrontOfPenguin(body):
    xValueToCheckForWall = body["you"]["x"]
    yValueToCheckForWall = body["you"]["y"]
    bodyDirection = body["you"]["direction"]

    if bodyDirection == "top":
        yValueToCheckForWall -= 1
    elif bodyDirection == "bottom":
        yValueToCheckForWall += 1
    elif bodyDirection == "left":
        xValueToCheckForWall -= 1
    elif bodyDirection == "right":
        xValueToCheckForWall += 1
    return doesCellContainWall(body["walls"], xValueToCheckForWall, yValueToCheckForWall)

def moveTowardsPoint(body, pointX, pointY):
    penguinPositionX = body["you"]["x"]
    penguinPositionY = body["you"]["y"]
    plannedAction = PASS
    bodyDirection = body["you"]["direction"]

    if penguinPositionX < pointX:
        plannedAction =  MOVE_RIGHT[bodyDirection]
    elif penguinPositionX > pointX:
        plannedAction = MOVE_LEFT[bodyDirection]
    elif penguinPositionY < pointY:
        plannedAction = MOVE_DOWN[bodyDirection]
    elif penguinPositionY > pointY:
        plannedAction = MOVE_UP[bodyDirection]

    if plannedAction == ADVANCE and wallInFrontOfPenguin(body):
        plannedAction = SHOOT
    return plannedAction

def moveTowardsCenterOfMap(body):
    centerPointX = math.floor(body["mapWidth"] / 2)
    centerPointY = math.floor(body["mapHeight"] / 2)
    return moveTowardsPoint(body, centerPointX, centerPointY)

def closestPowerup(body):
    """
    gives x, y for closest powerup
    """
    bonus_list = body["bonusTiles"]
    if len(bonus_list) == 0:
        return -1, -1

    you = body['you']
    x = you['x']
    y = you['y']

    m = 1000000
    m_bonus = bonus_list[0]
    for bonus in bonus_list:
        d = sqrt((x - bonus['x'])**2 + (y - bonus['y'])**2)
        if d < m:
            m = d
            m_bonus = bonus

    print("Closest powerup:", m_bonus['type'], "@", m_bonus['x'], m_bonus['y'], "dist=", m)
    return m_bonus['x'], m_bonus['y']



def findClosestPower(body):
    hearts = [b for b in body["bonusTiles"] if b['type'] == 'weapon-power']
    if len(hearts) == 0:
        return -1, -1

    you = body['you']
    x = you['x']
    y = you['y']

    m = 1000000
    m_heart = hearts[0]
    for heart in hearts:
        d = sqrt((x - heart['x'])**2 + (y - heart['y'])**2)
        if d < m:
            m = d
            m_heart = heart

    return m_heart['x'], m_heart['y']

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


# noinspection PyInterpreter
def shootIfPossible(body):
    you = body["you"]
    direction = you["direction"]
    myPosX = you["x"]
    myPosY = you["y"]
    enemy = body["enemies"][0]
    try:
        enX = enemy["x"]
        enY = enemy["y"]
    except:
        return False

    if direction == "right" and enX - myPosX > 0 and enY == myPosY:
        print("Shooting")
        return True
    elif direction == "left" and enX - myPosX < 0 and enY == myPosY:
        print("Shooting")
        return True
    elif direction == "bottom" and enY - myPosY > 0 and enX == myPosX:
        print("Shooting")
        return True
    elif direction == "top" and enY - myPosY < 0 and enX == myPosX:
        print("Shooting")
        return True
    else:
        return False


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