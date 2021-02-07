#!/usr/bin/python

"""

"""
import sys, os
#sys.path.insert(0, "./python")


import uproot4
import numpy as np
import awkward1 as ak
import matplotlib.pyplot as plt
##############dummy arguments a recuperer
# ROOT file name
# FEB ID
# index feb slot
# index_carte_side
# index_carte_up
# index_carte_corner
# threshold
# testType
if sys.argv[1] =='help' :
    print('Arguments to be passed in this order')
    print(' ROOT file name')
    print(' FEB ID ')
    print(' index feb slot ')
    print(' index_carte_side')
    print(' index_carte_up')
    print(' index_carte_corner ')
    print(' threshold ')
    print(' testType (RAMRandom or RAMOnOff)')
else :
    fileName = str(sys.argv[1])+':DAQ'
    feb_id = sys.argv[2]
    index_feb_slot = int(sys.argv[3])
    index_carte_side = int(sys.argv[4])
    index_carte_up = int(sys.argv[5])
    index_carte_corner = int(sys.argv[6])
    threshold = int(sys.argv[7])
    testType = str(sys.argv[8])
######################

    file = uproot4.open(fileName)
    llt=file.arrays()
    chs   = ak.to_numpy(llt.ch[:,0+index_feb_slot:32+index_feb_slot])

    chs_up = ak.to_numpy(llt.ch[:,index_carte_up:index_carte_up+4])
    chs_corner = ak.to_numpy(llt.ch[:,index_carte_corner])
    chs_side = ak.to_numpy(llt.ch[:,index_carte_side:index_carte_side+29:4])

    chs_A = chs

    chs_B = chs
    chs_B = np.delete(chs_B,np.s_[0:29:4],axis=1)
    chs_B = np.insert(chs_B,[3,6,9,12,15,18,21,24],chs_side[:,:],axis=1)

    chs_C = chs
    chs_C = np.delete(chs_C,np.s_[0:4],axis=1)
    chs_C = np.append(chs_C,chs_up,axis=1)

    chs_D = chs_B
    chs_D = np.delete(chs_D,np.s_[0:4],axis=1)
    chs_D = np.append(chs_D,chs_up[:,1:4],axis=1)
    chs_D = np.vstack([chs_D.T,chs_corner]).T


    cands = chs_A+chs_B+chs_C+chs_D

    etmax = np.max(cands,axis=1)
    add   = np.argmax(cands,axis=1)
    ettot = np.sum(chs,axis=1)

    mult = np.count_nonzero( chs >= threshold , axis = 1 )

    llt_etmax = ak.to_numpy(llt.etmax[:,0])
    llt_ettot = ak.to_numpy(llt.ettot[:,0])
    llt_add   = ak.to_numpy(llt.add[:,0])
    llt_mult   = ak.to_numpy(llt.mult[:,0])

    #print( "Number of errors for ETMAX = {0}".format(np.count_nonzero(llt_etmax != etmax)))
    #print( "Number of errors for ETTOT = {0}".format(np.count_nonzero(llt_ettot != ettot)))
    #print( "Number of errors for ADD   = {0}".format(np.count_nonzero(llt_add != add)))
    #print( "Number of errors for MULTIPLICTY   = {0}".format(np.count_nonzero(llt_mult != mult)))

    nEvts = llt_etmax.size

    if (llt_etmax.size != llt_ettot.size) : print( " problem in processing ETMAX vs ETTOT")
    if (llt_etmax.size != llt_add.size) : print( " problem in processing ETMAX vs ADD")
    if (llt_ettot.size != llt_add.size) : print("  problem in processing ETTOT vs ADD")

    fracErr_etmax = np.count_nonzero(llt_etmax != etmax)/nEvts
    fracErr_ettot = np.count_nonzero(llt_ettot != ettot)/nEvts
    fracErr_add = np.count_nonzero(llt_add != add)/nEvts
    fracErr_mult = np.count_nonzero(llt_mult != mult)/nEvts

    print( "Fraction of ETMAX error = {0}".format(fracErr_etmax))
    print( "Fraction of ETTOT error = {0}".format(fracErr_ettot))
    print( "Fraction of ADD error = {0}".format(fracErr_add))
    print( "Fraction of MULT error = {0}".format(fracErr_mult))
    fracErr_type = ["ETMAX","ETTOT","ADD","MULT"]
    fracErr = [fracErr_etmax, fracErr_ettot ,fracErr_add,fracErr_mult]


    plt.figure(figsize=(15,12))
    plt.subplot(321)
    plt.hist(llt_ettot,100)
    plt.xlabel('LLT ettot')
    plt.subplot(322)
    plt.hist(llt_etmax,100)
    plt.xlabel('LLT etmax')
    plt.subplot(323)
    plt.hist(llt_mult,100)
    plt.xlabel('LLT mult')
    plt.subplot(324)
    plt.hist(llt_add,32)
    plt.xlabel('LLT add')
    plt.axis([-1,32,0,100000])
    plt.subplot(325)
    plt.hist(fracErr_type, 10,weights=fracErr)
    plt.xlabel('Error fraction')
    #plt.show()
    outputFile = 'LLT_'+testType+'_FEB_' + str(feb_id) + '_Threshold_' + str(threshold) + '.pdf'
    plt.savefig(outputFile)
