import itertools, os
from glob import glob

def parse_scenarios(template, basedir, ext=".gpkg"):
    scenario_parse = [i.split('/')[-1].split('.')[0].split('_') for i in glob(os.path.join(basedir, f'*{ext}'))]
    scenarios = dict()
    for idx, k in enumerate(template.split('_')):
        if "$" in k:
            scenarios[k.replace("$", "").replace('{', '').replace('}', '')] = list(set([i[idx] for i in scenario_parse]))
    return scenarios

def compute_cartesian_product(scenarios):
    keys = scenarios.keys()
    values = scenarios.values()
    cross_product = itertools.product(*values)
    return [dict(zip(keys, items)) for items in cross_product]