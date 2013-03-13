import csv
import ipdb

def readcsvpres(f):
	d = {}
	n=0
	for row in csv.reader(f,delimiter='\t'):
		c_id = row[3]
		text = row[5]
		coname = row[2]
		# ipdb.set_trace()
		master = row[8]

		json = {'text':text, 'master':master, 'coname' : coname}
		if c_id in d:
			d[c_id].append(json)
		else:
			d[c_id] = [json]
		if n%1000 == 0:
			print n

		n+=1
	return d


def readcsvqa(f):
	d = {}
	n=0
	for row in csv.reader(f,delimiter='\t'):
		c_id = row[5]
		text = row[8]
		coname = row[2]
		# ipdb.set_trace()
		master = row[10]

		json = {'text':text, 'master':master, 'coname' : coname}
		if c_id in d:
			d[c_id].append(json)
		else:
			d[c_id] = [json]
		if n%1000 == 0:
			print n

		n+=1
	return d



f = open('../full_dataset_matched_modifiedtabPRES.txt')

presd = readcsvpres(f)

f = open('../full_dataset_matched_modifiedtabQA.txt')

qad = readcsvqa(f)