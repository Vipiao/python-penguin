import math
from movement import *




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
        d = math.sqrt((x - bonus['x'])**2 + (y - bonus['y'])**2)
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
        d = math.sqrt((x - heart['x'])**2 + (y - heart['y'])**2)
        if d < m:
            m = d
            m_heart = heart

    return m_heart['x'], m_heart['y']


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

