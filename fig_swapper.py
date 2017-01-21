#!/usr/lib/python2.7

# fig_swapper.py

# holy shit, this is going to be shitty.  Basically expecting it to fail.
# purpose: take the fig IDs from the DIAMOND subsystems results and get more info, so I can parse it into categories

import sys, time, re

try:
	fig_dic_file = open(sys.argv[1], "r")
	infile_name = sys.argv[2]
	role_name = sys.argv[3]
	hierarchy_name = sys.argv[4]
except IndexError:
	sys.exit("fig dic as argv1, diamond results file as argv2, subsystems2role as argv3, hierarchy file as argv4")

fig_dic = {}

t0 = time.clock()

for line in fig_dic_file:
	splitline = line.split("\t")
	try:
		if splitline[3] == "":
			fig_dic[splitline[0]] = "NULL"
		else:
			fig_dic[splitline[0]] = splitline[3]
	except IndexError:
		fig_dic[splitline[0]] = "NULL"

fig_dic_file.close()

t1 = time.clock()

print "fig dic assembled, starting on infile comparisons"
print "time so far: " + str(t1-t0) + " seconds."

# works up to here without errors, yay, I guess

# now, getting the role from the FIG id, this is file subsystems2role
roles = open(role_name, "r")
roles_dic = {}
for line in roles:
	splitline = line.split("\t")
	try:
		roles_dic[splitline[3].strip()] = splitline[0] + "\t" + splitline[2] + "\t" + splitline[1]
	except IndexError:
		print line
		sys.exit()

roles.close()

print "success with roles dic"

# next up, gotta read the hierarchy file to build that hierarchy
hierarchy = open(hierarchy_name, "r")
hier_dic = {}

for line in hierarchy:
	splitline = line.split("\t")
	hier_dic[splitline[3]] = splitline[2] + "\t" + splitline[1] + "\t" + splitline[0]

hierarchy.close()

# now converting the DIAMOND results (after going through analysis_counter) to have all the hierarchy info

infile = open(infile_name, "r")
outfile = open(infile_name + ".converted", "w")
errors = 0
matching_errors = 0
notfound_errors = 0

for line in infile:
	splitline = line.strip().split("\t")
	
	#first, check if there's any entry in subsystems.complex.figs associated with this ID
	try:
		level4 = fig_dic[splitline[2]]
	except KeyError:
		strippedline = line.strip()
		print str(strippedline) + "\tNOT FOUND"
		outfile.write(line.strip() + "\tNOT FOUND\n")
		notfound_errors += 1
		continue
	
	#next, see if that entry is in the hierarchy file
	try:
		hierarchy_entry = roles_dic[level4]
		outfile.write(line.strip() + "\t" + fig_dic[splitline[2]] + "\t" + hierarchy_entry + "\n")
	except KeyError:
		
		#wait, maybe we can save it if a slash is the issue!
		if ("/" in level4) or ("@" in level4) or (";" in level4) or ("##" in level4):
			entry = re.split('/|@|;|##', level4)[0][:-1]
#			entry = fig_dic[splitline[2]].split("/")[0][:-1]
			try:
				hierarchy_entry = roles_dic[entry]
				outfile.write(line.strip() + "\t" + level4 + "\t" + hierarchy_entry + "\n")
			except KeyError:
				#sometimes it's the second half of the slash part
				try:
					entry2 = re.split('/|@|;|##', level4)[1][1:]
				except IndexError:
					print level4
					print entry
					print "Issue at line 105"
					sys.exit()
				try:
					hierarchy_entry = roles_dic[entry2]
					outfile.write(line.strip() + "\t" + level4 + "\t" + hierarchy_entry + "\n")
				except KeyError:
					#sometimes they have a comma that needs removal
					t_entry = entry.split(",")[0]
					try:
						hierarchy_entry = roles_dic[t_entry]
						outfile.write(line.strip() + "\t" +  level4 + "\t" + hierarchy_entry + "\n")
					except KeyError:
						#at this point, god, who knows?
						matching_errors += 1
				
		# otherwise nope, couldn't save it
		else:
			try:
				hierarchy_entry = hier_dic[level4]
				outfile.write(line.strip() + "\t" + level4 + "\t" + hierarchy_entry + "\n")
			except KeyError:
				errors += 1
				print line.strip()
				print level4
				print " "
				outfile.write(line.strip() + "\t" + level4 + "\tNO HIERARCHY FOUND\n")

t2 = time.clock()

print "all done"
print "time for second part: " + str(t2-t1) + " seconds."
print "number of fig IDs not found to have any match: " + str(notfound_errors)
print "number of hierarchy errors (no match in hierarchy file): " + str(errors)
print "number of errors after all my trying things: " + str(matching_errors)

infile.close()
outfile.close()

