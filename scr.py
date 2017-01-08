#!/usr/bin/python
import os, sys, getopt, re, json, csv
from utils import Utils

# Config
with open('script.config', 'r') as fp:
	CONFIG = json.load(fp)

# Init script
for initial_path in ["output", "resource"]:
	if not os.path.exists(initial_path):
		os.makedirs(initial_path)

if not os.path.exists("resource/names.tsv"):
	print("Cannot find the names.tsv. We will download for you.")
	command = """cd resource && wget {} -O names.tsv.gz && gzip -d names.tsv.gz && cd ..""".format(CONFIG['names_tsv_url'])
	os.system(command)
	if os.path.exists("resource/names.tsv"):
		print("We get the file.")
	else:
		print("We cannot get the file.")
		sys.exit(1)

# parameterization
metabolite_name = sys.argv[1]
down_tsv = False
inc_syn = True
inc_prec = True
if len(sys.argv) > 2:
	sys_args = sys.argv[2]
	combinations = ['','-msp', '-mps', '-smp', '-spm', '-pms', '-psm', '-sp', '-ps']
	if sys_args in combinations or sys_args == "--download-tsv":
		inc_syn = True
		inc_prec = True
		if sys_args == "--download-tsv":
			down_tsv = True
	elif sys_args in ('-ms', '-sm', '-s'):
		inc_prec = False
	elif sys_args in ('-mp', '-pm', '-p'):
		inc_syn = False
	elif sys_args == '-m':
		inc_syn = False
		inc_prec = False
	else:
		raise Exception("please try again with right parameters")

if len(sys.argv) > 3:
	sys_args = sys.argv[3]
	if sys_args == '--download-tsv':
		down_tsv = True
	else:
		down_tsv = False

with open('output/{}.json'.format(metabolite_name), 'w') as fp:
	json.dump(Utils(metabolite_name, synonym=inc_syn, precursor=inc_prec).result, fp, indent=4)

os.system("python prepare_output.py '{}'".format(metabolite_name))


# clean unnecessary files
os.system("rm -rf output/*.txt")

def download_names_tsv():
	print "asdasdasd"
"""

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
