import csv
import ipdb

def readcsv(f, cid_row, text_row, master_row, coname_row):
	d = {}
	n=0
	for row in csv.reader(f,delimiter='\t'):
		c_id = row[cid_row]
		text = row[text_row]
		coname = row[coname_row]
		# ipdb.set_trace()
		master = row[master_row]
		n+=1

		if c_id in d:
			if master in d[c_id]:
				d[c_id][master] += ' ' + text
			else:
				d[c_id][master] = text
		else:
			d[c_id] = {}

		if n%100000 == 0:
			print n
	return d

f = open('../full_dataset_matched_modifiedtabPRES.txt')

presd = readcsv(f, 3, 5, 8, 2)

f = open('../full_dataset_matched_modifiedtabQA.txt')

qad = readcsv(f, 5, 7, 10, 2)