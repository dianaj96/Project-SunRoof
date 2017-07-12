# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 16:48:28 2016

@author: Recruiter-One
"""

import csv

divisor = 2500

outfileno = 1
outfile = None

with open('Addresses.csv', 'r') as infile:
    for index, row in enumerate(csv.reader(infile)):
        if index % divisor == 0:
            if outfile is not None:
                outfile.close()
            outfilename = 'Dbase-{}.csv'.format(outfileno)
            outfile = open(outfilename, 'w', newline='')
            outfileno += 1
            writer = csv.writer(outfile)
        writer.writerow(row)