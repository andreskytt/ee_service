import json
import codecs

def convert(definition, content):
	with codecs.open(definition, encoding='LATIN4') as f:
		cols = f.readlines()

	c = {'CPSV':cols[0].split('\t')[1].strip()}

	firstDone = False
	with codecs.open(content, encoding='UTF-16') as f:
		os = []
		for line in f:
			if not firstDone:
				firstDone = True
				continue

			data = line.strip().split('\t')
			o = {}
			o['@context'] = c  
			o['@id'] = data.pop(0)

			t = 1
			for d in data:
				if d:
					(tp, n) = cols[t].split('\t')
					if tp:
						o[n.strip()] = {'@type':'CPSV:' + tp, '@value': d}
					else:
						o[n.strip()] = d
				t = t + 1

			os.append(o)

	return os

#output = convert('AgentDef.txt', 'agent.txt')
#output.extend(convert('PSDef.txt', 'ps.txt'))

#output = convert('MKMDef.txt', 'mkm_svc.txt')
#output.extend(convert('AgentDef.txt','mkm_agent.txt'))
output = convert('AgentDef.txt', 'mkm_agent.txt')
output.extend(convert('MKMDef.txt', 'mkm_svc.txt'))

print json.dumps(output, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ': ')).encode('utf-8')
