import json
import string 

with open('../rasa_knowledge_base.json', 'r') as fr:
    data = json.load(fr)

data = data['apps']
names = []
featuresArray = []
for x in data:
    names += [x['name']]
    for fts in x['features']:
        fts = fts.translate(str.maketrans('', '', string.punctuation))
        featuresArray.append(fts)

print(names)

features = set(featuresArray)
print(features)

f = open('nlu.yml', 'w')

f.write("version: '3.0' \n\n" +
    "nlu:\n" +
    "- intent: greet\n" +
    "  examples: |\n" +
    "    - hey\n" +
    "    - hello\n" +
    "    - hi\n" +
    "    - hello there\n" +
    "    - good morning\n" +
    "    - good evening\n" +
    "    - moin\n" +
    "    - hey there\n" +
    "    - let's go\n" +
    "    - hey dude\n" +
    "    - goodmorning\n" +
    "    - goodevening\n" +
    "    - good afternoon\n" 
)

find_feature = [
    'Ask [app]{"entity": "object_type", "value": "apps"} to activate [<features>]{"entity": "features", "value": "<features>"}',
    'I want [app]{"entity": "object_type", "value": "apps"} to enable [<features>]{"entity": "features", "value": "<features>"}',
    'enable [apps](object_type) [<features>]{"entity": "features", "value": "<features>"}',
    'activate [apps](object_type) [<features>]{"entity": "features", "value": "<features>"}',
    'turn on [apps](object_type) [<features>]{"entity": "features", "value": "<features>"}',
    'authorize [apps](object_type) [<features>]{"entity": "features", "value": "<features>"}',
]
    
specify_feature = {
    "replace_features": [
        'Whichever has [<features>]{"entity": "features", "value": "<features>"}',
        'The one with [<features>]{"entity": "features", "value": "<features>"}',
        'with [<features>]{"entity": "features", "value": "<features>"}',
        'Is there one with [<features>]{"entity": "features", "value": "<features>"}'
    ],
    "replace_name": [
        'I want to launch [<name>]{"entity": "name", "value": "<name>"}',
        'Launch [<name>]{"entity": "name", "value": "<name>"}',
        'Open [<name>]{"entity": "name", "value": "<name>"}',
        'Please open [<name>]{"entity": "name", "value": "<name>"}',
        'Please launch [<name>]{"entity": "name", "value": "<name>"}'
    ],
    "no_replace": [
        'the [first]{"entity": "mention", "value": "1"} one',
        'The [second]{"entity": "mention", "value": "2"} one',
        'The [ninth]{"entity": "mention", "value": "9"} one',
        'number [1](mention)',
        'number [2](mention)',
        'the [last]{"entity": "mention", "value": "LAST"} one',
        '[any]{"entity": "mention", "value": "ANY"} of them will do'
    ]
}

f.write('\n- intent: find_feature\n'+
        '  examples: |\n' 
)

for p in find_feature:
    for fts in features:
        replacedStr = p.replace('<features>', fts)
        f.write('    - ' + replacedStr + '\n')

f.write('\n- intent: specify_feature\n'+
        '  examples: | \n'
)

for p in specify_feature['replace_features']:
    for fts in features:
        replacedStr = p.replace('<features>', fts)
        f.write('    - ' + replacedStr + '\n')

for p in specify_feature['replace_name']:
    for n in names:
        replacedStr = p.replace('<name>', n)
        f.write('    - ' + replacedStr + '\n')

for p in specify_feature['no_replace']:
    f.write('    - ' + p + '\n')

f.write('\n- intent: out_of_scope\n' +
        '  examples: |\n' +
        '    - adsfg\n' +
        '    - I want to order good\n' +
        '    - What is 2+2?\n' +
        "    - Who's the US President?)\n"
)
f.close()
