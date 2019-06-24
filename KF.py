import matplotlib.pyplot as plt
import numpy as np

#initialize mu [x,y,vx,vy] and sigma (-8000,-3000 are coordinate adjustments for the second player being tracked)
mu = np.array([0,0,0,0,-8000,-3000,0,0])[None]
sigma = np.identity(8)
estimated = [[],[],[],[]]

def main():
	#reading the ground truth and control input data files (both are ~ 2x840 arrays)
	truth1 = np.loadtxt('loc.txt')
	control1 = np.loadtxt('change.txt')
	truth2 = np.loadtxt('loc2_copy.txt')
	print(len(truth2[0]))
	truth2[0] += -8000
	truth2[1] += -3000
	control2 = np.loadtxt('change2_copy.txt')
	truth = np.array([truth1[0],truth1[1],truth2[0],truth2[1]])
	control = np.array([control1[0],control1[1],control2[0],control2[1]])

	#initialize R and Q matrices
	R = np.array([[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]])*50
	Q = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])*50

	#call the prediction for each step then update every 10th step
	for i in range(len(control[0])):
		sample_u = np.random.normal(0,.01,4)
		control_step = np.array([control[0][i]+sample_u[0],control[1][i]+sample_u[1],control[2][i]+sample_u[2],control[3][i]+sample_u[3]])		
		control_step = control_step.T
		prediction(control_step,R)
		print([len(control[0]),len(control[1]),len(control[2]),len(control[3])])
		#call measurment update every 10 frames (arbitrary number)
		if(i%10 == 0):
			sample_z = np.random.normal(0, 50, 4)
			truth_step = np.array([truth[0][i]+sample_z[0],truth[1][i]+sample_z[1],truth[2][i]+sample_z[2],truth[3][i]+sample_z[3]])
			truth_step = truth_step.T
			update(truth_step,Q)
	plot(truth)

#takes in the controls (change in (dX,dY)) as variable 'c' and does prediction then reassigns mu and sigma
def prediction(c,r):
	global mu
	global sigma
	global estimated
	#variable for the amount of frames that elapse between information (will tweak to see differences)
	delt = 1
	A = np.array([[1,0,delt,0,0,0,0,0],[0,1,0,delt,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,delt,0],[0,0,0,0,0,1,0,delt],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]])
	B = np.array([[0,0,0,0],[0,0,0,0],[delt,0,0,0],[0,delt,0,0],[0,0,0,0],[0,0,0,0],[0,0,delt,0],[0,0,0,delt]])
	#column vector of the noise terms in R
	#noise = np.array([[r[0][0]],[r[1][1]],[r[2][2]],[r[3][3]]])
	print("Velocity " + str(mu[0]))
	print("Velocity " + str(mu[0]))
	#new_x = mu[0][0] + delt*mu[0][2] + r[0][0]
	#new_y = mu[0][1] + delt*mu[0][3] + r[0][0]
	#new_vx = mu[0][2] + c[0]
	#new_vy = mu[0][3] + c[1]
	#new_mu = [[new_x,new_y,new_vx,new_vy]]
	#mu = new_mu
	#calculating mu bar then assigning
	mu_bar = np.dot(A,mu[0]) + np.dot(B,c)
	print(np.dot(A,mu[0]).shape, np.dot(B,c).shape, mu.shape)
	#print("This" + str(np.dot(A,mu[0])))
	mu = mu_bar[None]
	#another = np.array([[1,2,1,1],[0,1,2,3],[3,4,5,6],[1,2,4,5]])
	#print("This is noise: " + str(noise.T))
	sig_bar = np.dot(A,np.dot(sigma,A.T)) + r
	estimated[0].append(mu[0][0])
	estimated[1].append(mu[0][1])
	estimated[2].append(mu[0][4])
	estimated[3].append(mu[0][5])

def update(t,q):
	global mu
	global sigma
	#motion model matrix (partial identity)
	H = np.array([[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0]])
	#compute Kalman Gain (for "weighing" residual term later)
	K = np.dot(np.dot(sigma,H.T),np.linalg.inv(np.dot(H,np.dot(sigma,H.T)) + q))
	print(K)
	print(t)
	print(mu)
	print(np.dot(H,mu[0]))
	print(mu[0].shape, H.shape, np.dot(H,mu[0]).shape)
	#vector representation of the difference between truth and estimated
	diff = t - np.dot(H,mu[0])
	new_mu = mu[0] + np.dot(K,diff)
	mu = new_mu[None]
	sigma = np.dot((np.identity(8)-np.dot(K,H)),sigma)

def plot(truth):
	global estimated
	estimated = np.array(estimated)
	#calculate error
	err = []
	for i in range(len(truth[0])):
		yd = truth[1][i] - estimated[1][i]
		xd = truth[0][i] - estimated[0][i]
		err.append(np.absolute(yd) + np.absolute(xd))
	me = np.sum(err)/len(err)
	print("Here is the Mean Error: " + str(me))
	#error graph of distance from ground truth (in pixels)
	iterations = len(truth[0])
	plt.figure(1)
	plt.plot(range(iterations),err,"r--")
	plt.xlabel("Iteration #")
	plt.ylabel("Sum of Pixel Error")
	#plotting ground truth and estimated (w/ every frame used for prediction)
	plt.figure(2)
	plt.plot(estimated[0],estimated[1],'b-', label = "Kalman Filter P1")
	plt.plot(estimated[2],estimated[3],'g-', label = "Kalman Filter P2")
	plt.legend(loc="upper left")
	plt.show()

main()