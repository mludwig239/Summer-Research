import numpy as np
import matplotlib.pyplot as plt
import random

def main():
    trend1 = eGreedy(0.1,1)
    trend2 = eGreedy(0.1,0.95)
    plot(trend1,trend2)

    #simple epsilon greedy if (d=1 then no decay so should be able to make this function the same and call it twice from main with different d) pseudocode in the robotics textbook, essentially just pick one then keep exploiting that unless e chosen then pick randomly to update others
def eGreedy(e,d):
    expectations = np.zeros(5) #estimation of distributions for each of the 5 players
    times_drawn = np.zeros(5) #number of times drawn for finding average
    optimal_list = np.zeros(1000) #average reward at each draw
    opt_choice = np.random.randint(1,6) #the current optimal choice
    reward_sum = 0
    for i in range(1000):
        #check if optimal choice has changed
        max_slot = np.argmax(expectations)+1
        if(max_slot != opt_choice):
            opt_choice = max_slot #updating the value for which is the current greedy choice
        randE = np.random.randint(1,101)
        #explore option
        if(randE > 100-100*e):
            players = [1,2,3,4,5]
            players.remove(opt_choice)
            explore = random.choice(players)
            if(explore == 1):
                val = np.random.uniform(-0.2,0.8) #draw value
            if(explore == 2):
                val = np.random.normal(0,1)
            if(explore == 3):
                val = np.random.uniform(0.2,0.4)
            if(explore == 4):
                val = np.random.normal(0.3,2)
            if(explore == 5):
                val = np.random.normal(0.15,0.25)
            choice_sum = expectations[explore-1]*times_drawn[explore-1]+val
            times_drawn[explore-1] += 1 #says that has been drawn from an additional time
            expectations[explore-1] = choice_sum/times_drawn[explore-1]
            reward_sum += val
            optimal_list[i] = reward_sum/(i+1) #creating the progression of average reward
        #choose optimally   
        else:
            if(opt_choice == 1):
                val = np.random.uniform(-0.2,0.8) #draw value
            if(opt_choice == 2):
                val = np.random.normal(0,1)
            if(opt_choice == 3):
                val = np.random.uniform(0.2,0.4)
            if(opt_choice == 4):
                val = np.random.normal(0.3,2)
            if(opt_choice == 5):
                val = np.random.normal(0.15,0.25)
            choice_sum = expectations[opt_choice-1]*times_drawn[opt_choice-1]+val
            times_drawn[opt_choice-1] += 1
            expectations[opt_choice-1] = choice_sum/times_drawn[opt_choice-1]
            reward_sum += val
            optimal_list[i] = reward_sum/(i+1)
        #decay exploration rate
        e *= d
        print("Iteration")
    return optimal_list
    
def plot(line1,line2):
    numIter = range(1000)
    plt.plot(numIter,line1,label='eps=0.9',color='blue')
    plt.plot(numIter,line2,label='w/ decay',color='black')
    plt.xlabel("Choice Number")
    plt.ylabel("Average Reward")
    plt.legend(loc="upper right")
    plt.title("Epsilon Greedy")
    plt.savefig("epsgreedy.png", bbox_inches = 'tight')
    plt.show()
    
main()