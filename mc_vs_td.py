import numpy as np
def main():
    #2D list where each row represents an inning (sequence of events with rewards)
    sequences = [[("GB",0),("K",0),("GB",0),("GB",0)],[("BB",0),("K",0),("PU",0),("K",0)],[("GB",0),("BB",0),("PU",2),("PU",0),("PU",0)],[("PU",0),("PU",1),("LD",0),("LD",0),("K",0),("BB",0),("K",0)],[("K",0),("PU",0),("K",0)],[("GB",0),("BB",0),("GB",1),("BB",0),("GB",0),("K",0)],[("PU",0),("GB",0),("GB",0)],[("K",0),("K",0),("GB",0)],[("K",0),("K",0),("GB",0)],[("GB",0),("K",0),("GB",0),("BB",0),("K",0)],[("K",0),("PU",1),("GB",0),("GB",0)],[("GB",0),("GB",0),("GB",0)],[("BB",0),("GB",0),("K",0),("LD",0)],[("LD",0),("PU",1),("K",0),("K",0)],[("LD",0),("GB",0),("K",0)],[("GB",0),("LD",0),("LD",1),("BB",0),("GB",1),("PU",0),("BB",0),("GB",0)],[("PU",0),("GB",0),("GB",0)],[("GB",0),("K",0),("K",0)]]
    transitions = [["GB","K","GB","GB"],["BB","K","PU","K"],["GB","BB","PU","PU","PU"],["PU","PU","LD","LD","K","BB","K"],["K","PU","K"],["GB","BB","GB","BB","GB","K"],["PU","GB","GB"],["K","K","GB"],["K","K","GB"],["GB","K","GB","BB","K"],["K","PU","GB","GB"],["GB","GB","GB"],["BB","GB","K","LD"],["LD","PU","K","K"],["LD","GB","K"],["GB","LD","LD","BB","GB","PU","BB","GB"],["PU","GB","GB"],["GB","K","K"]]
    #return a dictionary with actions and values determined through two different methods
    mc = monteCarlo(sequences)
    td = tdLearn(transitions, mc)
    print("Monte Carlo Results:")
    print(mc)
    print("Temporal-Difference Results:")
    print(td)

def monteCarlo(seq):
    #First-visit Monte Carlo valuation for sequences of actions and rewards (no state included) EX: (A,1)
    #create dictionary and add entries for each unique new thing encountered (for loop with if statements)
    ht = {"K":[0,0],"BB":[0,0],"GB":[0,0],"LD":[0,0],"PU":[0,0]}
    for i in seq:
        #index keeper in each list to access scores
        for event in i:
            #access the tuples for each of events (total runs over times referenced)
            if(event[0] == "K"):
                cur = ht.get("K")
                cur[0] += event[1]
                cur[1] += 1
                ht["K"] = cur
            elif(event[0] == "BB"):
                cur = ht.get("BB")
                cur[0] += event[1]
                cur[1] += 1
                ht["BB"] = cur
            elif(event[0] == "GB"):
                cur = ht.get("GB")
                cur[0] += event[1]
                cur[1] += 1
                ht["GB"] = cur
            elif(event[0] == "LD"):
                cur = ht.get("LD")
                cur[0] += event[1]
                cur[1] += 1
                ht["LD"] = cur
            elif(event[0] == "PU"):
                cur = ht.get("PU")
                cur[0] += event[1]
                cur[1] += 1
                ht["PU"] = cur
    #dictionary with the values calculated then added
    valueDic = {"K":0,"BB":0,"GB":0,"LD":0,"PU":0}
    k = ht.get("K")
    bb = ht.get("BB")
    gb = ht.get("GB")
    ld = ht.get("LD")
    pu = ht.get("PU")
    valueDic["K"] = np.round(np.divide(k[0],k[1]),3)
    valueDic["BB"] = np.round(np.divide(bb[0],bb[1]),3)
    valueDic["GB"] = np.round(np.divide(gb[0],gb[1]),3)
    valueDic["LD"] = np.round(np.divide(ld[0],ld[1]),3)
    valueDic["PU"] = np.round(np.divide(pu[0],pu[1]),3)
    #return dictionary of hit type with only value  
    return valueDic
    
def tdLearn(trans,vals):
    #Valuing certain types of hit using td(0) (graphical structure/transitions considered)
    #2D array treated as transition probability matrix (K, BB, GB, LO, PU)
    #dictionary with the row associated with each outcome
    coor = {"K":0,"BB":1,"GB":2,"LD":3,"PU":4}
    transMat = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    justVals = list(vals.values())
    for inning in trans:
        hitter = 0
        while(hitter < len(inning)-1):
            #coordinates in the matrix
            x = coor.get(inning[hitter])
            y = coor.get(inning[hitter+1])
            transMat[x][y] += 1
            hitter += 1
    #turn matrix into proportions (each row should sum to 1)
    for row,outcome in enumerate(transMat):
        transMat[row] = np.divide(outcome,float(sum(outcome)))
    results = [0,0,0,0,0]
    things = ["K","BB","GB","LD","PU"]
    for item in range(len(transMat)):
        results[item] = justVals[item] + np.sum(transMat[item]*justVals)
    results = np.round(results,3)
    td_value = {"K":results[0],"BB":results[1],"GB":results[2],"LD":results[3],"PU":results[4]}
    return td_value
main()