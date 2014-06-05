#reworked from http://blog.ionelmc.ro/2014/05/25/python-packaging/

import re
from itertools import product, chain
from jinja2 import FileSystemLoader, Environment
jinja = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)

pythons = ['2.6', '2.7', '3.2', '3.3', '3.4']
#pythons = ['2.7']
deps = [
    'whoosh>=2.6,<2.7',
]
covers = [True, False]
envs = [''] # could be some env vars that activate certain features

skips=[]

# the list of environments is the product of python versions,
# dependencies, coverage switches (on/off) and
# environment variables

matrix = {}
for python, dep, cover, env in product(pythons, deps, covers, envs):
    if (python, dep, cover, env) not in skips:
        name = '-'.join(filter(None, (  # mangle the python version, deps,
                                        # cover flags and env vars into
                                        # something pretty
            python,
            '-'.join(re.sub(
                r'[A-Za-z/:.>]+[/=](.*?)(,.*|/.*)?$',
                r'\1',
                dep
            ).split(' ')), # strip useless characters
            '' if cover else 'nocover',
            env and env.lower().replace('_', ''),
        )))

        matrix[name] = {
            'python': 'python' + python if 'py' not in python else python,
            'deps': dep.split(),
            'cover': cover,
            'env': env,
        }

for k in matrix :
    print(k,matrix[k])

with open('tox.ini', 'w') as fh:
    fh.write(jinja.get_template('tox.tmpl.ini').render(matrix=matrix))

with open('.travis.yml', 'w') as fh:
    fh.write(jinja.get_template('.travis.tmpl.yml').render(matrix=matrix))

