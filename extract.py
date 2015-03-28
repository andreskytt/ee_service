import json
import codecs
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def convert(definition, content, previous=None):

	with codecs.open(definition, encoding='LATIN4') as f:
		cols = f.readlines()

	(cpsv, tpe) = re.match("(.*)\/(\w*)$",cols[0].split('\t')[1].strip()).group(1,2)
	c = {'CPSV':cpsv}

	firstDone = False
	with codecs.open(content, encoding='UTF-16') as f:
		if previous is None:
			os = []
		else:
			os = previous

		for line in f:
			if not firstDone:
				firstDone = True
				continue

			data = line.strip().split('\t')
			this_id = data.pop(0)
			o = {}
			o['@context'] = c  
			o['@id'] = this_id
			o['@type'] = tpe

			t = 1
			for d in data:
				if d:
					def_line = cols[t].split('\t')
					if len(def_line) > 2:
						ref = def_line[2]
					else:
						ref = ""
					
					(tp, n) = (def_line[0], def_line[1])

					if ref:
						for target in os:
							if target['@id'] == d:
								(ref_type, ref_name) = ref.strip().split(":")
								if ref_name in target.keys():
									target[ref_name]['@value'].append(this_id)
								else:
									target[ref_name] = {'@type':'CPSV:' + ref_type, '@value': [this_id]}

					if tp:
						o[n.strip()] = {'@type':'CPSV:' + tp, '@value': d}
					else:
						o[n.strip()] = d


				t = t + 1

			os.append(o)

	return os

#output = convert('AgentDef.txt', 'agent.txt')
#output.extend(convert('PSDef.txt', 'ps.txt'))

output = convert('AgentDef.txt', 'mkm_agent.txt')
output = convert('MKMDef.txt', 'mkm_svc.txt', output)

print json.dumps(output, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ': ')).encode('utf-8')
