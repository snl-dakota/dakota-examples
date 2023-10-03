import numpy as np
from math import sin

def Ishigami(x,y,z):
    a=7.0
    b=0.1
    return sin(x) + a*sin(y)**2 + b*z**4*sin(x)


def random_samples(num_samples):
    bounds = np.array([[-3.141592,3.141592],[-3.141592,3.141592],[-3.141592,3.141592]])
    sample = np.random.uniform(bounds[:,0],bounds[:,1],(num_samples, len(bounds)))
    print(bounds)
    return sample

#number of samples
sample = random_samples(10000)
labels = np.zeros(len(sample))
sample = np.column_stack((sample,labels))

#add Ishigami function output to sample points
for i in range(len(sample)):
    sample[i][3] = Ishigami(sample[i][0],sample[i][1],sample[i][2])

#save sample file to build ML model from
np.savetxt("IshigamiSample.txt", sample, delimiter='\t', fmt='%.10f')
