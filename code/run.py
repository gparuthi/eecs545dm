import csv
from ujson import dumps
from datetime import datetime
from financial_tone import analyst_tone,POSITIVE,NEGATIVE
from IPython import parallel
import test

# merge dictionary with gathered data
def load_dic(presd, merged):
	for cid in presd:
	    if cid not in merged:
	        merged[cid] = {}
		for mas in presd[cid]:
			if mas in merged[cid]:
				merged[cid][mas] += ' ' + presd[cid][mas]
			else:
				merged[cid][mas] = presd[cid][mas]

# single core sentiment naive sentiment analysis
def start(merged):
	c = 0
	res = {}
	for cid in merged:
	    anal_text = ''
	    manager_text = ''
	    res[cid] = {}
	    if 'Analyst' in merged[cid]:
	        anal_text = merged[cid]['Analyst']
	        #print anal_text
	    
	    if 'CEO-Chair' in merged[cid]:
	        manager_text += merged[cid]['CEO-Chair']
	    if 'Finance' in merged[cid]:
	        manager_text += merged[cid]['Finance']
	    if 'Operator' in merged[cid]:
	        manager_text += merged[cid]['Operator']

	    ana_tone = analyst_tone(POSITIVE, NEGATIVE, anal_text)
	    manager_tone = analyst_tone(POSITIVE, NEGATIVE, manager_text)        
	    res[cid]['a_tone'] = ana_tone
	    res[cid]['m_tone'] = manager_tone   
	    c += 1
	    if c%100 == 0:
			print '[%s] %d / %d' % (str(datetime.now()), c,len(merged))
	return res


def getSent(item):
	# import log
	from datetime import datetime
	from financial_tone import analyst_tone,POSITIVE,NEGATIVE
	# logger = log.logger('./logs/Sentiment_'+str(datetime.now()))
	# logger.log('starting now..')
	c = 0
	res = {}
	cid= item[0]
	anal_text = ''
	manager_text = ''
	res[cid] = {}

	if 'Analyst' in item[1]:
	    anal_text = item[1]['Analyst']
	    #print anal_text

	if 'CEO-Chair' in item[1]:
	    manager_text += item[1]['CEO-Chair']

	if 'Finance' in item[1]:
	    manager_text += item[1]['Finance']
	    
	if 'Operator' in item[1]:
	    manager_text += item[1]['Operator']

	ana_tone = analyst_tone(POSITIVE, NEGATIVE, anal_text)
	manager_tone = analyst_tone(POSITIVE, NEGATIVE, manager_text)        
	res[cid]['a_tone'] = ana_tone
	res[cid]['m_tone'] = manager_tone   
	print '[%s] %s' % (str(datetime.now()), res[cid])
	return res


def get_merged(presd,qad):
	merged = {}
	load_dic(presd, merged)
	load_dic(qad, merged)

	return merged

def StartParallelProcess():
    print datetime.now()
    parallel_result = dview.map_async(getSent, items)
    parallel_result.wait_interactive()
    print datetime.now()
    return parallel_result

# dict is {cid:{'a_tone':'','m_tone':''}}
def write_to_file(dict, output_filep):
	# output_filep = 'output.csv'
	with open(output_filep, "wb") as f:
	    fileWriter = csv.writer(f, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
	    for k in dict:
	        row = k.keys()
	        # ipdb.set_trace()
	        row.append(k[k.keys()[0]]['a_tone'])
	        row.append(k[k.keys()[0]]['m_tone'])

	        fileWriter.writerow(row)
# code for init a parallel sentiment analysis
# parallel core sentiment analysis 
rc= parallel.Client()
lview = rc.load_balanced_view() 
lview.block = True
dview = rc[:]

merged = get_merged(test.presd, test.qad)
items = merged.items()



# res = processFile.map([])