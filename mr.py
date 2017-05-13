#!/usr/bin/python -tt

# Basic edit distance, and Wagner-Fischer fucntion copied from: http://www.giovannicarmantini.com/2016/01/minimum-edit-distance-in-python
# The rest is for the MR-WER library 
# Copyright (C) 2017, Qatar Computing Research Institute, HBKU (author: Ahmed Ali)
#

from __future__ import division
import sys  
reload(sys)
import codecs
import collections
import re
from subprocess import call
import numpy as np
sys.setdefaultencoding('utf8')


def wagner_fischer(r, h):
    n = len(r) + 1  # counting empty string 
    m = len(h) + 1  # counting empty string
 
    # initialize D matrix
    D = np.zeros(shape=(n, m), dtype=np.int)
    D[:,0] = range(n)
    D[0,:] = range(m)
 
    # B is the backtrack matrix. At each index, it contains a triple
    # of booleans, used as flags. if B(i,j) = (1, 1, 0) for example,
    # the distance computed in D(i,j) came from a deletion or a
    # substitution. This is used to compute backtracking later.
    B = np.zeros(shape=(n, m), dtype=[("del", 'b'), 
                                      ("sub", 'b'),
                                      ("ins", 'b')])
    B[1:,0] = (1, 0, 0) 
    B[0,1:] = (0, 0, 1)
 
    for i, l_1 in enumerate(r, start=1):
        for j, l_2 in enumerate(h, start=1):
            deletion = D[i-1,j] + 1
            insertion = D[i, j-1] + 1
            substitution = D[i-1,j-1] + (0 if l_1==l_2 else 2)
 
            mo = np.min([deletion, insertion, substitution])
 
            B[i,j] = (deletion==mo, substitution==mo, insertion==mo)
            D[i,j] = mo

    return D, B
    
def naive_backtrace(B_matrix):
    i, j = B_matrix.shape[0]-1, B_matrix.shape[1]-1
    backtrace_idxs = [(i, j)]
 
    while (i, j) != (0, 0):
        if B_matrix[i,j][1]:
            i, j = i-1, j-1
        elif B_matrix[i,j][0]:
            i, j = i-1, j
        elif B_matrix[i,j][2]:
            i, j = i, j-1
        backtrace_idxs.append((i,j))
 
    return backtrace_idxs

def align(r, h, bt):
 
    aligned_r = []
    aligned_h = []
    operations = []
 
    backtrace = bt[::-1]  # make it a forward trace
    i=d=s=c=0
 
    for k in range(len(backtrace) - 1): 
        i_0, j_0 = backtrace[k]
        i_1, j_1 = backtrace[k+1]
 
        r_w = None
        h_w = None
        op = None
        
 
        if i_1 > i_0 and j_1 > j_0:  # either substitution or no-op
            if r[i_0] == h[j_0]:  # no-op, same symbol
                r_w = r[i_0]
                h_w = h[j_0]
                op = "c"
                c+=1
            else:  # cost increased: substitution
                r_w = r[i_0]
                h_w = h[j_0]
                op = "s"
                s+=1
        elif i_0 == i_1:  # insertion
            r_w = " "
            h_w = h[j_0]
            op = "i"
            i+=1
        else: #  j_0 == j_1,  deletion
            r_w = r[i_0]
            h_w = " "
            op = "d"
            d+=1
 
        aligned_r.append(r_w)
        aligned_h.append(h_w)
        operations.append(op)
    
    return i,d,s,c,aligned_r, aligned_h, operations

def merge_align(align_ref,sentence_id,nref):
    hypID={}
    m_align_ref={}
    for ref_id in range(nref):
        m_align_ref['file_'+str(ref_id)]={}
        d=c=0
        for idx, val in enumerate(align_ref['file_'+str(ref_id)]['sent_'+sentence_id]['aligned_h']): 
            if align_ref['file_'+str(ref_id)]['sent_'+sentence_id]['operations'][idx] == 'd':
                d+=1
                delcount=str(d).zfill(2)
                reccount=str(c).zfill(2)
                t=reccount+"-"+delcount+" <DEL>"
                m_align_ref['file_'+str(ref_id)][t]=align_ref['file_'+str(ref_id)]['sent_'+sentence_id]['aligned_r'][idx]
                hypID[t]=1
            else:
                c+=1
                reccount=str(c).zfill(2)
                hypID[reccount]=1
                m_align_ref['file_'+str(ref_id)][reccount]=align_ref['file_'+str(ref_id)]['sent_'+sentence_id]['operations'][idx]

    od = collections.OrderedDict(sorted(hypID.items()))
    i=d=s=c=di=0
    align_compact=""
    for key, value in od.items(): #we loop over all words in the hypothesis
        all_errors=""
        for ref_id in range(nref):
            if key in m_align_ref['file_'+str(ref_id)]: all_errors=all_errors+" "+m_align_ref['file_'+str(ref_id)][key]
            else:all_errors=all_errors+" NULL"
        align_compact+=key+" "+all_errors+"\n"
        #print(key, all_errors)
        if "<DEL>" in key:
            if "NULL" in all_errors: di+=1
            else: d+=1
        else:
            if "c" in all_errors: c+=1
            elif "s" in all_errors: s+=1
            else: i+=1
        
   
    return i,d,s,c,di,align_compact,align_compact

