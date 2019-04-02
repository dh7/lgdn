import json
import codecs

def create_question(prefix):
    with open('{}_00/questions.json'.format(prefix),'rt', encoding="ascii") as json_file:
        questions = json.load(json_file)
    for i, q in enumerate(questions):
        print(i, questions[i])
        q_id = u'{}_{:02d}'.format(prefix, i)
        a = u'<li><a href="https://storage.googleapis.com/lgdn-eu/dataviz.html?prefix=' + q_id + u'"\n' + \
        u' target="dataviz" onclick="closeNav(this)")>\n' + \
            questions[i] + u'\n</a></li>\n'
        global html
        html += a

html = u'<h2>La transition &eacute;cologique</h2><ul>'
create_question('ECO')
html += '</ul>'

html += u'<h2>La fiscalité et les dépenses publiques</h2><ul>'
create_question('FIS')
html += '</ul>'

html += u'<h2>La démocratie et la citoyenneté</h2><ul>'
create_question('DEM')
html += '</ul>'

html += u"<h2>L'organisation de l'État et des services publics</h2><ul>"
create_question('ORG')
html += '</ul>'

with codecs.open('questions.html','w',encoding='utf-8') as file:
    file.write(html)
