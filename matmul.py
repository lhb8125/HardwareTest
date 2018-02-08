#coding=utf-8

import os,commands,time,threading,argparse

import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("n",help="set number of matrix multiplications")
args = parser.parse_args()
bottleneck = int(args.n)


def calculate():
    a = np.random.random((30000,30000))
    b = np.random.random((30000,30000))
    np.matmul(a,b)


for i in range(bottleneck):
    calculate()


