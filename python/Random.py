#! /usr/bin/env python

import sys
import math
import numpy as np
import matplotlib.pyplot as plt

#################
# Random class
#################
# class that can generate random numbers
class Random:
    """A random number generator class"""

    # initialization method for Random class
    def __init__(self, seed = 5555):
        self.seed = seed
        self.m_v = np.uint64(4101842887655102017)
        self.m_w = np.uint64(1)
        self.m_u = np.uint64(1)
        
        self.m_u = np.uint64(self.seed) ^ self.m_v
        self.int64()
        self.m_v = self.m_u
        self.int64()
        self.m_w = self.m_v
        self.int64()

    # function returns a random 64 bit integer
    def int64(self):
        with np.errstate(over='ignore'):
            self.m_u = np.uint64(self.m_u * np.uint64(2862933555777941757) + np.uint64(7046029254386353087))
        self.m_v ^= self.m_v >> np.uint64(17)
        self.m_v ^= self.m_v << np.uint64(31)
        self.m_v ^= self.m_v >> np.uint64(8)
        self.m_w = np.uint64(np.uint64(4294957665)*(self.m_w & np.uint64(0xffffffff))) + np.uint64((self.m_w >> np.uint64(32)))
        x = np.uint64(self.m_u ^ (self.m_u << np.uint64(21)))
        x ^= x >> np.uint64(35)
        x ^= x << np.uint64(4)
        with np.errstate(over='ignore'):
            return (x + self.m_v)^self.m_w

    # function returns a random floating point number between (0, 1) (uniform)
    def rand(self):
        return 5.42101086242752217E-20 * self.int64()

    # function returns a random integer (0 or 1) according to a Bernoulli distr.
    def Bernoulli(self, p=0.5):
        if p < 0. or p > 1.:
            return 1
        
        R = self.rand()

        if R < p:
            return 1
        else:
            return 0

    # function returns a random double (0 to infty) according to an exponential distribution
    def Exponential(self, beta=1.):
      # make sure beta is consistent with an exponential
      if beta <= 0.:
        beta = 1.

      R = self.rand();

      while R <= 0.:
        R = self.rand()

      X = -math.log(R)/beta

      return X

    # function returns a random integer using normal distribution (Box-muller)
    def normal(self, mu=2., sigma=0.5):
        if sigma <= 0.:
            sigma = 0.5
        
        R1 = self.rand();
        R2 = self.rand();
        
        y1 = np.sqrt(-2*np.log(R1))*np.cos(2*np.pi*R2)
        y2 = np.sqrt(-2*np.log(R1))*np.sin(2*np.pi*R2)
        
        X = y1*sigma+mu
        return X
# main function for this Python code
if __name__ == "__main__":
    # if the user includes the flag -h or --help print the options
    if '-h' in sys.argv or '--help' in sys.argv:
        print ("Usage: %s [-seed number]" % sys.argv[0])
        print
        sys.exit(1)

    # default seed
    seed = 5555

    # read the user-provided seed from the command line (if there)
    if '-seed' in sys.argv:
        p = sys.argv.index('-seed')
        seed = sys.argv[p+1]

    # set random seed for numpy
    np.random.seed(seed)

    # class instance of our Random class using seed
    random = Random(seed)

    # create some random data
    N = 50000

    # an array of random numbers from numpy
    x = np.random.rand(N)

################################################################
    # open a file for writing and assign it to random numbers
    random_numbers = open('random_Gaussian.txt', 'w')

    # an array of random numbers using our Random class
    try:
        for i in range(0,N):
            line = str(random.normal())
            random_numbers.write(line)
            random_numbers.write("\n")
            #print(line)
    except ValueError:
        print("Invalid input")

    random_numbers.close()
    

# read from generated random number txt file
print("\nReading the file..." )

out =[]
with open('random_Gaussian.txt') as f:
    for line in f:
        out.append(float(line))

print("\nPlotting..." )
print("\nPlot saved!")
# create histogram of our data
plt.figure(figsize=[10,8])
plt.style.use('ggplot')
n, bins, patches = plt.hist(out, 50, density=True, facecolor='c', alpha=0.75)

# plot formating options
plt.xlabel('Data')
plt.ylabel('Probability')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.title('Histogram of random number Gaussian distribution')
plt.grid(True)
plt.savefig('Gaussian_random_number.png')

