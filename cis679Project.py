n = 5
e = 0.1

import numpy as np

def price(player, actions, bids):
  sumVal = 0
  for ind, val in enumerate(actions[0]):
    if val != 2 and ind != player:
      sumVal += bids[0, ind]
  return sumVal + e

def beta(player, actions, bids):
  sumOpen = 0
  for ind, val in enumerate(actions[0]):
    if val == 1:
      sumOpen += bids[0, ind]
  if sumOpen > 0:
    return (bids[0, player] / sumOpen)
  else:
    return 0
  
def utility(actions, player, bids):
  if actions[0, player] == 0:
    sumPart = 0
    for ind, val in enumerate(actions[0]):
      if val != 2:
        sumPart += bids[0, ind]
    return sumPart - price(player, actions, bids)
  elif actions[0, player] == 1:
    sumOpen = 0
    sumProp = 0
    for ind, val in enumerate(actions[0]):
      if val == 0:
        sumProp += price(ind, actions, bids)
      elif val == 1:
        sumOpen += bids[0,ind]
    return sumOpen + beta(player, actions, bids)*sumProp
  elif actions[0, player] == 2:
    return 0
  else:
    raise ValueError("Only three available actions")

#==============================================================================
# def findActionIndex(actList, actArray):
#     return actList.index(np.all(actArray))
#==============================================================================
def findActionIndex(actList, actArray):
    for i,j in enumerate(actList):
        if np.array_equal(j, actArray):
            return i
    return -1
    
actions = np.ones([1,n], dtype=int)*2
eqValues = []
eqActions = []
  
#Step 1: Randomly assign starting valuations
#values = np.ones([1,n], dtype=int)
values = np.ndarray(shape = (1,n), dtype=float, buffer=np.array([500,2,300,1,-303,4,8,6,9,8,5.4,1.2]))
 
#Step 2: Retreive bids
bids = values
  
#Step 3: Calculate equilibrium assignments
utilList = []
actList = []
for i in range(0, pow(3, n)):
    for k in range(n-1, -1, -1):
        if actions[0,k] == 2:
            actions[0,k] = 0
        else:
            actions[0,k] += 1
            break
    utilList.append(np.zeros([1,n]))
    actList.append(np.copy(actions))
    for j in range(0, n):
        utilList[i][0,j] = utility(actions, j, bids)

#actDict = {actArray: ind for ind,actArray in enumerate(actList)}
  
for ind, util in enumerate(utilList):
    actArray = np.copy(actList[ind])
    eqUtil = True
    #compare utility to possible alternatives
    for loc, x in enumerate(actArray[0]):
        #1st alternate action
        actArray[0, loc] = (x+1)%3
        index = findActionIndex(actList, actArray)

        if utilList[index][0,loc] > util[0,loc]:
            eqUtil = False
            break
        #2nd alternate action
        actArray[0, loc] = (x+2)%3
        index = findActionIndex(actList, actArray)
        if utilList[index][0,loc] > util[0,loc]:
            eqUtil = False
            break
        #original action
        actArray[0, loc] = (x+3)%3
    if eqUtil:
        eqValues.append(util)
        eqActions.append(actList[ind])
  
#Step 4: Output statistics
print("Number of players " + str(n))
print("Epsilon value " + str(e))
print("Starting values " + str(values))
print("Bids " + str(bids))
print("Equilibrium values " + str(eqValues))
print("Equilibrium actions " + str(eqActions))