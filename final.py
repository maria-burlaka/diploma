from __future__ import division
import itertools
import random
from collections import OrderedDict

import math
from numpy import *
from scipy import stats, special

def random_perm():
  perm = list(array)
  i=0
  while i<n-1:
    j=random.randint(i, n)
    perm[i], perm[j] = perm[j], perm[i]
    i += 1
  return perm

def modsumm(perm):
  modsumm=[]
  i=0
  while i<n:
    modsumm.append((perm[i]+array[i])%n)
    i+=1
  return modsumm
# makes list of modulo summs 

def alpha(modsumm):
  multiset={}
  for value in array:
    multiset[value]=modsumm.count(value)
  alpha={power: 0 for power in range(n+1)}
  for key in array:
    for power in range(n+1):
        if multiset[key]==power:
            alpha[power]+=1
  return alpha
# returns list of dictionaries {power: number of values with this power}

def alpha_tupple(alpha):
  keys = range(n+1)
  alpha_list = []
  for key in keys:
    alpha_list.append(alpha[key])
  alpha_tupple = tuple(alpha_list)
  return alpha_tupple
# returns tupple of alphas <a0, a1, ...>

def file_print():
  headers = ["Alpha tupple".center(int(round(n*3.5))), "Num of perms".center(15), "Confidence interval (n)".center(28), 
             "Confidence interval (p)".center(28)]
  f = open('intervals_{}.txt'.format(n), 'w')
  for header in headers:
    f.write(header)
  f.write('\n')
  for item in intervals:
    f.write(('$'+str(item[0])+'$&').center(int(round(n*3.5))))
    f.write((str(int(item[1]*N))+' &').center(15))
    f.write((str(item[2])+' &').center(28))
    f.write((str(item[3])+' &').center(28))
    f.write((str(item[4])+' \\\\').center(28))
    f.write('\n')
  f.close()


def confidence_intervals():
    confidence=0.05              
    intervals = []
    M = math.factorial(n)
    for item in sorted_alphas_count:
        p = sorted_alphas_count[item]
        intervals.append([item, p, [int(M*stats.chi2.ppf(confidence, 2*p*N)/(2*N - N*p + 1 + stats.chi2.ppf(confidence, 2*p*N)/2)),
                                   int(math.ceil(M*stats.chi2.ppf(1-confidence, 2*p*N+2)/(2*N - N*p + stats.chi2.ppf(1-confidence, 2*p*N+2)/2)))],
                                   [int(M*p - M*math.sqrt(p*(1-p)/N)*stats.norm.ppf(1-confidence/2)), 
                                    int(math.ceil(M*p + M*math.sqrt(p*(1-p)/N)*stats.norm.ppf(1-confidence/2)))], 
                                   [int(stats.chi2.ppf(confidence/2, 2*p*N) *M/(2*N)), 
                                    int(math.ceil(stats.chi2.ppf(1-confidence/2, 2*p*N+2) *M/(2*N)))],
                                   [int(M/N*stats.binom.interval(1-confidence, N, p)[0]), 
                                    int(math.ceil(M/N*stats.binom.interval(1-confidence, N, p)[1]))]
                        ])

    return intervals


n = 55
N = 10**7

array = range(n)
alphas_count = {}
for l in range(N):
  random_per = random_perm()
  modsum = modsumm(random_per)
  alph = alpha(modsum)
  alpha_tupp = alpha_tupple(alph)
  if alpha_tupp in alphas_count:
    alphas_count[alpha_tupp] += 1
  else:
    alphas_count[alpha_tupp] = 1
sorted_alphas_count = OrderedDict(sorted(alphas_count.items(), key=lambda x: x[1], reverse=True))
for key in sorted_alphas_count:
  sorted_alphas_count[key] /= N
intervals = confidence_intervals()
file_print()




