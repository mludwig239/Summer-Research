import numpy
import random
import pandas as pd

#dictionary recording all the scoring plays as keys with values of number of runs scored
scoringDict = {(0,0):1,(1,0):2,(2,0):2,(3,0):2,(4,0):3,(5,0):3,(6,0):3,(7,0):4,(1,2):1,(1,3):1,(2,1):1,(2,2):1,(2,3):1,(3,8):1,(3,1):1,(3,2):1,(3,3):1,(4,5):1,(4,2):2,(4,3):2,(5,5):1,(5,2):2,(5,3):2,(5,9):1,(5,16):1,(6,1):2,(6,2):2,(6,3):2,(6,10):1,(7,2):3,(7,3):3,(7,5):2,(7,12):1,(7,19):1,(8,8):1,(9,8):2,(10,8):2,(11,8):2,(12,8):3,(13,8):3,(14,8):3,(15,8):4,(9,10):1,(9,11):1,(10,9):1,(10,10):1,(10,11):1,(11,16):1,(11,9):1,(11,10):1,(11,11):1,(12,10):2,(12,11):2,(12,13):1,(13,17):1,(13,13):1,(13,10):2,(13,11):2,(14,9):2,(14,10):2,(14,11):2,(14,18):1,(15,10):3,(15,11):3,(15,13):2,(15,15):1,(15,20):1,(16,16):1,(17,16):2,(18,16):2,(19,16):2,(20,16):3,(21,16):3,(22,16):3,(23,16):4,(17,18):1,(17,19):1,(18,17):1,(18,18):1,(18,19):1,(19,17):1,(19,18):1,(19,19):1,(20,18):2,(20,19):2,(20,21):1,(21,18):2,(21,19):2,(21,21):1,(22,17):2,(22,18):2,(22,19):2,(23,23):1,(23,18):3,(23,19):3,(23,21):2}

#list of tuples with two team IDs to simulate a game between them
schedule = [(0,1),(0,1),(0,2),(0,2),(0,3),(0,3),(0,4),(0,4),(0,5),(0,5),(1,2),(1,2),(1,3),(1,3),(1,4),(1,4),(1,5),(1,5),(2,3),(2,3),(2,4),(2,4),(2,5),(2,5),(3,4),(3,4),(3,5),(3,5),(4,5),(4,5),(0,3),(0,3),(0,3),(1,2),(1,2),(1,2),(4,5),(4,5),(4,5)]
#dictionary of each teams abbreviation along with their teamID
teamName = {0:"NYY",1:"CHC",2:"LAD",3:"HOU",4:"WSH",5:"CLE"}

#list variable storing each teams wins
gamesWon = [0,0,0,0,0,0]
    
#variables storing game score
teamOneRuns = 0
teamTwoRuns = 0
inning = 1

def main():
    #get entire schedule then with for loop run every game into the function gameSimulation
    for x in schedule:
        gameSimulation(x[0],x[1])
    print("Final Season Results")
    print("--------------------")
    print("American League:")
    print("Yankees: " + str(gamesWon[0]) + " - " + str(13-gamesWon[0]))
    print("Astros: " + str(gamesWon[3]) + " - " + str(13-gamesWon[3]))
    print("Indians: " + str(gamesWon[5]) + " - " + str(13-gamesWon[5]))
    print("--------------------")
    print("National League:")
    print("Cubs: " + str(gamesWon[1]) + " - " + str(13-gamesWon[1]))
    print("Dodgers: " + str(gamesWon[2]) + " - " + str(13-gamesWon[2]))
    print("Nationals: " + str(gamesWon[4]) + " - " + str(13-gamesWon[4]))

def gameSimulation(tOne,tTwo):
    global teamOneRuns
    global teamTwoRuns
    global inning
    global gamesWon
    teamOneRuns = 0
    teamTwoRuns = 0
    inning = 1
    #populate matrices from excel file data
    teamOne = populateRosterMatrix(tOne)
    teamTwo = populateRosterMatrix(tTwo)
    teamOneLineupSpot = 0
    teamTwoLineupSpot = 0
    tie = False
    #simulate game
    while(inning < 19):
        #do simulate for half inning (including updating runsThisInning then appending at end of loop) until get to absorbing state then if inning%2==0 its bottom half (stanton in this case) and add score to his run total then increment inning variable
        currentState = 0
        returnedStateOne = 0
        returnedStateTwo = 0
        #do work for top half (judge)
        if((inning % 2) != 0):
            while(returnedStateOne != 24):
                returnedStateOne = gameProgression(currentState, teamOne[teamOneLineupSpot%9])
#check if returned state is 24 and if it is then increment innings to move on to next half
                runsScored(currentState,returnedStateOne)
                teamOneLineupSpot += 1
                currentState = returnedStateOne
            teamOneLineupSpot += 1
            inning += 1
        else:
            while(returnedStateTwo != 24):
                returnedStateTwo = gameProgression(currentState, teamTwo[teamTwoLineupSpot%9])
                runsScored(currentState,returnedStateTwo)
                teamTwoLineupSpot += 1
                currentState = returnedStateTwo
            teamTwoLineupSpot += 1
            inning += 1
    if(teamOneRuns == teamTwoRuns):
        tie = True
        print("Going to Extras")
    #extra innings check
    while(tie == True):
        currentState = 0
        returnedStateOne = 0
        returnedStateTwo = 0
        #simulate an inning then check if scores are still tied (if not matching change variable to true)
        if((inning % 2) != 0):
            while(returnedStateOne != 24):
                returnedStateOne = gameProgression(currentState, teamOne[teamOneLineupSpot%9])
#check if returned state is 24 and if it is then increment innings to move on to next half
                runsScored(currentState,returnedStateOne)
                teamOneLineupSpot += 1
                currentState = returnedStateOne
            teamOneLineupSpot += 1
            inning += 1
        else:
            while(returnedStateTwo != 24):
                returnedStateTwo = gameProgression(currentState, teamTwo[teamTwoLineupSpot%9])
                runsScored(currentState,returnedStateTwo)
                teamTwoLineupSpot += 1
                currentState = returnedStateTwo
            teamTwoLineupSpot += 1
            inning += 1
        if(teamOneRuns != teamTwoRuns):
            tie = False
    if(teamOneRuns > teamTwoRuns):
        gamesWon[tOne] += 1
    else:
        gamesWon[tTwo] += 1
    print("Game Over!")
    print("-----------")
    print("| " + teamName.get(tOne) + " || " + str(teamOneRuns) + " |")
    print("| " + teamName.get(tTwo) + " || " + str(teamTwoRuns) + " |")
    print("-----------")

def gameProgression(currentState, player):
    #simulate to find new state to switch to and call runs scoring function which modifies global scoring variables given currentState input and newState (which will be returned at end of function)
    line = player[currentState:currentState+1]
    line = list(line)
    line = line[0]
    #line = list(player[currentState:currentState+1])[0]
    scenario = 0
    play = random.randint(1,1000)/1000.000
    currentTotal = 0
    #iterate until you find the randomly chosen scenario
    while(currentTotal < play):
        #print("In Loop")
        #never making it out of in loop
        if((currentTotal+line[scenario]) >= play):
            #print("Got to New State")
            newState = scenario
            currentTotal += line[scenario]
        else:
            currentTotal += line[scenario]
            scenario += 1 
    #if(newState != 24):
       # runsScored(currentState, newState)
    return newState

def runsScored(currentState, newState):
    #make tuple of (currentState, newState) then check the dictionary if any key matches then if it does get corresponding value and appened to that players run total (based on which inning it is)
    global scoringDict
    global teamOneRuns
    global teamTwoRuns
    global inning
    transition = (currentState, newState)
    if((inning % 2) != 0):
        #print("Runs Scored Called")
        if transition in scoringDict:
            teamOneRuns += scoringDict.get(transition)
            #print("added runs")
    else:
        if transition in scoringDict:
            teamTwoRuns += scoringDict.get(transition)

def populateRosterMatrix(teamID):
    #read .csv and create list of matrices for each player in the team (lineup in order of listing in file)
    teamDF = pd.read_csv("sim_stats_roster.csv")
    playerDF = pd.DataFrame(teamDF[teamDF.Team == teamID])
    playerID = 0
    playerMatrixList = []
    while(playerID < 9):
        appearances = playerDF.iloc[playerID]["Appearances"]
        hr = round(playerDF.iloc[playerID]["HR"]/appearances,3)
        single = round(playerDF.iloc[playerID]["Single"]/appearances,3)
        double = round(playerDF.iloc[playerID]["Double"]/appearances,3)
        triple = round(playerDF.iloc[playerID]["Triple"]/appearances,3)
        walk = round(playerDF.iloc[playerID]["Walk"]/appearances,3)
        sacrifice = round(playerDF.iloc[playerID]["Sacrifice"]/appearances,3)
        dp = round(playerDF.iloc[playerID]["DP"]/appearances,3)
        playerMatrix = numpy.asarray([[hr, round(single+walk,3), double, triple, 0, 0, 0, 0, round(1-(hr+single+walk+double+triple),3), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [hr, 0, double, triple, walk, single, 0, 0, 0, round(1-(hr+single+walk+double+triple+dp),3), 0, 0, 0, 0, 0, 0, dp, 0, 0, 0, 0, 0, 0, 0, 0], [hr, single, double, triple, walk, 0, 0, 0, 0, 0, round(1-(hr+single+walk+double+triple),3), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [hr, single, double, triple, 0, walk, 0, 0, sacrifice, 0, 0, round(1-(hr+single+walk+double+triple+sacrifice),3), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [hr, 0, double, triple, 0, single, 0, walk, 0, 0, 0, 0, round(1-(hr+single+walk+double+triple+dp),3), 0, 0, 0, 0, 0, 0, dp, 0, 0, 0, 0, 0.002], [hr, 0, double, triple, 0, single, 0, walk, 0, sacrifice, 0, 0, 0, round(1-(hr+single+walk+double+triple+sacrifice+dp),3), 0, 0, dp, 0, 0, 0, 0, 0, 0, 0, 0.002], [hr, single, double, triple, 0, 0, 0, walk, 0, 0, sacrifice, 0, 0, 0, round(1-(hr+single+walk+double+triple+sacrifice),3), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [hr, 0, double, triple, 0, single, 0, walk, 0, 0, 0, 0, sacrifice, 0, 0, round(1-(hr+single+walk+double+triple+sacrifice+dp),3), 0, 0, 0, dp, 0, 0, 0, 0, 0.002], [0, 0, 0, 0, 0, 0, 0, 0, hr, round(single+walk,3), double, triple, 0, 0, 0, 0, round(1-(hr+single+walk+double+triple),3), 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, hr, 0, double, triple, walk, single, 0, 0, 0, round(1-(hr+single+walk+double+triple+dp),3), 0, 0, 0, 0, 0, 0, dp], [0, 0, 0, 0, 0, 0, 0, 0, hr, single, double, triple, walk, 0, 0, 0, 0, 0, round(1-(hr+single+walk+double+triple),3), 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, hr, single, double, triple, 0, walk, 0, 0, sacrifice, 0, 0, round(1-(hr+single+walk+double+triple+sacrifice),3), 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, hr, 0, double, triple, 0, single, 0, walk, 0, 0, 0, 0, round(1-(hr+single+walk+double+triple+dp),3), 0, 0, 0, dp], [0, 0, 0, 0, 0, 0, 0, 0, hr, 0, double, triple, 0, single, 0, walk, 0, sacrifice, 0, 0, 0, round(1-(hr+single+walk+double+triple+sacrifice+dp),3), 0, 0, dp], [0, 0, 0, 0, 0, 0, 0, 0, hr, single, double, triple, 0, 0, 0, walk, 0, 0, sacrifice, 0, 0, 0, round(1-(hr+single+walk+double+triple+sacrifice),3), 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, hr, 0, double, triple, 0, single, 0, walk, 0, 0, 0, 0, sacrifice, 0, 0, round(1-(hr+single+walk+double+triple+dp),3), dp], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, hr, round(single+walk,3), double, triple, 0, 0, 0, 0,round(1-(hr+single+walk+double+triple),3)], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, hr, 0, double, triple, walk, single, 0, 0, round(1-(hr+single+walk+double+triple),3)], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, hr, single, double, triple, walk, 0, 0, 0, round(1-(hr+single+walk+double+triple),3)], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, hr, single, double, triple, 0, walk, 0, 0, round(1-(hr+single+walk+double+triple),3)], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, hr, 0, double, triple, 0, single, 0, walk, round(1-(hr+single+walk+double+triple),3)], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, hr, 0, double, triple, 0, single, 0, walk, round(1-(hr+single+walk+double+triple),3)], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, hr, single, double, triple, 0, 0, 0, walk, round(1-(hr+single+walk+double+triple),3)], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, hr, 0, double, triple, 0, single, 0, walk, round(1-(hr+single+walk+double+triple),3)], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
        playerMatrixList.append(playerMatrix)
        playerID += 1
    return playerMatrixList