#!/usr/bin/python
import os, sys, re, json, urllib2, getopt
from utils import Utils

# Environment variable
with open('script.config', 'r') as fp:
		CONFIG = json.load(fp)

__JAVA_HOME__ = CONFIG['java_bin']

__GETPRECURSOR_JAVA__ = "GetPrecursors"

# metabolite_name = "aspirin"
metabolite_name = sys.argv[1]


with open('{}.json'.format(metabolite_name), 'w') as fp:
	json.dump(Utils(metabolite_name).result, fp, indent=4)

os.system("python prepare_output.py '{}'".format(metabolite_name))

# print(Utils(metabolite_name).result)

"""
metabolite_name = sys.argv[1]
inc_syn = True
inc_prec = True
if len(sys.argv) > 2:
	sys_args = sys.argv[2]
	combinations = ['','-msp', '-mps', '-smp', '-spm', '-pms', '-psm']
	if sys_args in combinations:
		inc_syn = True
		inc_prec = True
	elif sys_args in ('-ms', '-sm', '-s'):
		inc_prec = False
	elif sys_args in ('-mp', '-pm', '-p'):
		inc_syn = False
	elif sys_args == '-m':
		inc_syn = False
		inc_prec = False
	else:
		raise Exception("please try again with right parameters")

def main(metabolite_name, **kwargs):

	if kwargs['inc_precursors'] and not kwargs['inc_synonyms']:
		print "pathway function will call with precursors"
	elif kwargs['inc_synonyms'] and not kwargs['inc_precursors']:
		print "pathway function will call with synonyms"
    elif kwargs['inc_precursors'] and kwargs['inc_synonyms']:
        print "pathway function will call synonyms and with precursors"
    else:
        print "pathway function will call with metabolite and its compound"

main(metabolite_name, inc_synonyms=inc_syn , inc_precursors=inc_prec)
"""

"""
returned_obj = {
	'metabolite_name': "glutamate", 
	'synonyms': [
                "2-ammoniopentanedioate", 
                "glutamate", 
                "glutamate(1-)", 
                "glutamic acid monoanion"
            ],
	'precursors': [
					{
						'parent' : {'type': "M", 'name': "glutamate"},
						'name': "(2S,3S)-3-Methylphenylalanine"
					},
					{
						'parent' : {'type': "S", 'name': "glutamate(1-)"},
						'name': "(2S,3S)-3-Methylphenylalanine"
					}
				],
	'pathways': [
					{
						'parent': {'type': "M/S/P", 'name': "glutamate"},
						'name': "",
						'url': "",
						'source': "Reactome/Wikipathways"
					}
			]
}
"""