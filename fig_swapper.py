#!/usr/lib/python2.7

# fig_swapper.py

# purpose: take the fig IDs from the DIAMOND subsystems results and get more info, so I can parse it into categories

import sys, time, re

try:
	fig_dic_file = open(sys.argv[1], "r")
	infile_name = sys.argv[2]
	role_name = sys.argv[3]
	hierarchy_name = sys.argv[4]
except IndexError:
	sys.exit("subsystems2peg as argv1, diamond results file as argv2, subsystems2role as argv3, hierarchy file as argv4")

# Step 1: get a reference dictionary of Fig IDs to level 3 hierarchy
# This step is using subsystems2peg.
fig_dic = {}

t0 = time.clock()

for line in fig_dic_file:
	splitline = line.split("\t")
	fig_dic[splitline[2]] = splitline[0]

fig_dic_file.close()

t1 = time.clock()

print "Fig ID disctionary assembled from subsystems2peg."
print "time so far: " + str(t1-t0) + " seconds."


# Step 2: build another reference dictionary, connecting level 3 hierarchy to level 4, and to levels 1/2
# This step is using subsystems2role.
roles = open(role_name, "r")
roles_dic = {}
roles_l4_dic = {}

for line in roles:
	splitline = line.split("\t")
	roles_l4_dic[splitline[0]] = splitline[3].strip()
	roles_dic[splitline[0]] = splitline[2] + "\t" + splitline[1]

roles.close()
print "Hierarchy read in from subsystems2role."


# Step 3: not all entries are in the subsystems2role file.  Some are in subsys.txt.  We need to get those, too.
# This step is using subsys.txt.
hierarchy = open(hierarchy_name, "r")
hier_dic = {}
hier_l4_dic = {}

for line in hierarchy:
	splitline = line.split("\t")
	hier_dic[splitline[2]] = splitline[1] + "\t" + splitline[0]
	hier_l4_dic[splitline[2]] = splitline[3].strip()

hierarchy.close()
print "Hierarchy read in from subsys.txt."


# Step 4: Now, we're going to read in our Fig IDs that we want to match to hierarchy, and print the converted info.
# This step uses an outfile from the SAMSA pipeline.  For your own use, just make sure that you're giving a 3-column tab-separated file as input, and the Fig ID is in the 3rd (final) column.
infile = open(infile_name, "r")
outfile = open(infile_name + ".converted", "w")
line_counter = 0
errors = 0

for line in infile:
	line_counter += 1
	splitline = line.strip().split("\t")
	
	#first, check if there's any entry in subsystems2peg associated with this ID
	try:
		level3 = fig_dic[splitline[2]]
	except KeyError:
		strippedline = line.strip()
		outfile.write(line.strip() + "\tNOT FOUND\n")
		errors += 1
		continue
	
	#next, see if that entry is in the subsystems2role file
	try:
		hierarchy_entry = roles_dic[level3]
		outfile.write(line.strip() + "\t" + roles_l4_dic[level3] + "\t" + level3 + "\t" + hierarchy_entry + "\n")
	except KeyError:
		
		# perhaps it's in the hierarchy file instead
		try:
			hierarchy_entry = hier_dic[level3]
			outfile.write(line.strip() + "\t" + hier_l4_dic[level3] + "\t" + level3 + "\t" + hierarchy_entry + "\n")
		except KeyError:
			
			# not found
			outfile.write(line.strip() + "\t" + level4 + "\tNO HIERARCHY FOUND\n")
			errors += 1

t2 = time.clock()

print "All done"
print "Time for second part: " + str(t2-t1) + " seconds."
print "Total number of lines read: " + str(line_counter)
print "Number of hierarchy errors (no match in hierarchy or subsystems2role files to the Fig ID): " + str(errors)

infile.close()
outfile.close()

