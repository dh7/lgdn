import json

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
    for key, value in input.iteritems()}
        elif isinstance(input, list):
                    return [byteify(element) for element in input]
        elif isinstance(input, unicode):
                    return input.encode('utf-8')
        else:
                    return input

with open('ECO_00/questions.json') as json_file:
    ECO = json.load(json_file)
with open('FIS_00/questions.json') as json_file:
    FIS = json.load(json_file)
with open('ORG_00/questions.json') as json_file:
    ORG = json.load(json_file)
with open('DEM_00/questions.json') as json_file:
    DEM = json.load(json_file)

html = u'<h2>La transition &eacute;cologique</h2>'
for i, q in enumerate(ECO):
    print(i, ECO[i],ECO[i][39])
    q_id = u'ECO_{:02d}'.format(i)
    a = u'<a href="https://storage.googleapis.com/lgdn/dataviz.html?prefix=' + q_id + u'"' + \
	u'target="dataviz" onclick="closeNav()">' + \
        ECO[i] + u'</a>\n'
    html += a
print (html)
print (html[189])
import codecs

with codecs.open('questions.html','w','utf8') as file:
    file.write(html)
