#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

# import our Random class from python/Random.py file
sys.path.append(".")
from python.MySort import MySort

# main function for our CookieAnalysis Python code
if __name__ == "__main__":
   
    haveInput = False

    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            continue

        InputFile = sys.argv[i]
        haveInput = True
    
    if '-h' in sys.argv or '--help' in sys.argv or not haveInput:
        print ("Usage: %s [options] [input file]" % sys.argv[0])
        print ("  options:")
        print ("   --help(-h)          print options")
        print
        sys.exit(1)
    
    Nmeas = 1
    times = []
    times_avg = []

    need_rate = True
    
    with open(InputFile) as ifile:
        for line in ifile:
            if need_rate:
                need_rate = False
                rate = float(line)
                continue
            
            lineVals = line.split()
            Nmeas = len(lineVals)
            t_avg = 0
            for v in lineVals:
                t_avg += float(v)
                times.append(float(v))

            t_avg /= Nmeas
            times_avg.append(t_avg)

    Sorter = MySort()

    times = Sorter.DefaultSort(times)
    times_avg = Sorter.DefaultSort(times_avg)
    # try some other methods! see how long they take
    # times_avg = Sorter.BubbleSort(times_avg)
    # times_avg = Sorter.InsertionSort(times_avg)
    # times_avg = Sorter.QuickSort(times_avg)

    # ADD YOUR CODE TO PLOT times AND times_avg HERE
    # calculate the 5th, 25th, 50th, 75th, and 95th percentiles of the distribution [index].

    quant_5  = int(0.05*(len(times_avg) +1))
    quant_25 = int(0.25*(len(times_avg) +1))
    quant_50 = int(0.5*(len(times_avg) +1))
    quant_75 = int(0.75*(len(times_avg) +1))
    quant_95 = int(0.95*(len(times_avg) +1))
    quant_997 = int(0.997*(len(times_avg) +1))
    
    #print(quant_5, quant_25, quant_50, quant_75,quant_95)
    mean = np.mean(times_avg)
    median = np.median(times_avg)
    std = np.std(times_avg)
    
    #print('mean, median, rms = ', mean, median, std)
    
    plt.figure(figsize=[10,8])

    plt.hist(times, color="b", bins=80, density=True,alpha=0.75)
    plt.legend()
    plt.xlabel("Time between missing cookies [days]")
    plt.ylabel("Probability")
    plt.title('Rate of 2.0 cookies/day')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.yscale('log')
    plt.grid(True)
    plt.show()
    plt.savefig('Times.png')
    
    plt.figure(figsize=[10,8])
    min_ylim, max_ylim = plt.ylim()
    plt.hist(times_avg, bins=80, histtype='stepfilled', color="g", density=True, alpha=0.75)
    plt.axvline(mean, color='r', linestyle='dashed', linewidth=1)
    plt.text(mean*0.9, max_ylim*0.3, 'Mean: {:.2f}'.format(mean))
    
    plt.axvline(times_avg[quant_5], color='b', linestyle='dashed', linewidth=1)
    plt.text(times_avg[quant_5]*0.5, max_ylim*0.05, '5th: {:.2f}'.format(times_avg[quant_5]))
    
    plt.axvline(times_avg[quant_25], color='w', linestyle='dashed', linewidth=1)
    plt.text(times_avg[quant_25]*0.8, max_ylim*0.1, '25th: {:.2f}'.format(times_avg[quant_25]))
    #plt.axvline(times_avg[quant_50], color='orange', linestyle='dashed', linewidth=1)
    plt.axvline(times_avg[quant_75], color='y', linestyle='dashed', linewidth=1)
    plt.text(times_avg[quant_75]*1., max_ylim*0.7, '75th: {:.2f}'.format(times_avg[quant_75]))
    
    plt.axvline(times_avg[quant_95], color='k', linestyle='dashed', linewidth=1)
    plt.text(times_avg[quant_95]*1., max_ylim*1.0, '95th: {:.2f}'.format(times_avg[quant_95]))
    
    plt.axvline(times_avg[quant_997], color='c', linestyle='dashed', linewidth=1)
    plt.text(times_avg[quant_997]*1., max_ylim*1.2, '99.7th: {:.2f}'.format(times_avg[quant_997]))
    plt.legend()
    plt.xlabel("Average time between missing cookies [days]")
    plt.ylabel("Probability")
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.title('10 measurements per experiment with Rate of 2.0 cookies/day')
    plt.yscale('log')
    plt.show()
    plt.savefig('Times_avg.png')


