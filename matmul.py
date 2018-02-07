#coding=utf-8

import os,commands,time,threading,argparse

import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("n",help="set number of matrix multiplications")
args = parser.parse_args()
bottleneck = args.n


def calculate():
    a = np.random.random((20000,20000))
    b = np.random.random((20000,20000))
    print(np.matmul(a,b))


for i in range(bottleneck):
    calculate()


