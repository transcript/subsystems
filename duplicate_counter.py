#!/usr/env Python

# duplicate_counter.py

import sys

infile_name = sys.argv[1]
infile = open(infile_name, "r")

outfile = open(infile_name + ".reduced", "w")

id_list = []
id_dic = {}
no_hier_dic = {}

duplicate_count = 0
unique_count = 0
no_hier_count = 0

for line in infile:
	if line[0] == ">":
		id = line.strip()
	else:
		if "NO HIERARCHY" in id:
			no_hier_dic[no_hier_count] = line.strip()
			no_hier_count += 1
		try:
			if line.strip() == id_dic[id]:
				duplicate_count += 1
				if duplicate_count < 10:
					print line
		except KeyError:
			id_dic[id] = line.strip()
			unique_count += 1
			continue

infile.close()
print "Done!"

for entry in id_dic.keys():
	outfile.write(entry + "\n" + id_dic[entry] + "\n")
outfile.close()
print "Outfile written."

print "Total number of unique seqs:\t" + str(unique_count)
print "Total number of duplicates:\t" + str(duplicate_count)

#print "Total number of unique seqs:\t" + str(len(set(id_list)))
#print "Total number of duplicates:\t" + str(len(id_list) - len(set(id_list)))

