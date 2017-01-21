#!/usr/lib/python2.7

# FIG_extractor.py

import sys, time

try:
	infile = open(sys.argv[1], "r")
except IndexError:
	sys.exit("Specify the subsystems.complex file as ARGV1.")

outfile = open(sys.argv[1] + ".figs", "w")

line_counter = 0

t0 = time.clock()

for line in infile:
	if line[0:3] == "fig":
		outfile.write(line)
	
	line_counter += 1
	if line_counter % 1000000 == 0:
		t1 = time.clock()
		print str(line_counter)[:-6] + "M lines processed in " + str(t1-t0) + " seconds."

print str(line_counter) + " lines processed."

infile.close()
outfile.close()