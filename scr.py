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
default_options = CONFIG['default_options']

def println(string, indent=0, color=""):
	print('{0}{1}{2}{3}'.format(" " * indent, color, string, Utils.bcolors.ENDC))

def download_names_tsv():
	command = """cd resource && wget {} -O names.tsv.gz && gzip -d names.tsv.gz && cd ..""".format(CONFIG['names_tsv_url'])
	os.system(command)
	if os.path.exists("resource/names.tsv"):
		println("We get the file.", color=Utils.bcolors.OKGREEN)
		println("#" * 60, color=Utils.bcolors.HEADER)
	else:
		println("We cannot get the file.", color=Utils.bcolors.FAIL)
		sys.exit(1)

if not os.path.exists("resource/names.tsv"):
	println("Cannot find the names.tsv. We will download for you.", color=Utils.bcolors.OKGREEN)
	download_names_tsv()


# default parameters
down_tsv = default_options['download_tsv'] # False
show_result = default_options['show_result'] # False
inc_syn = default_options['include_synonyms'] # True
inc_prec = default_options['include_precursors'] # True

if len(sys.argv) != 1:
	metabolite_name = sys.argv[1]
else:
	raise Exception(Utils.bcolors.FAIL + "Please specify at least a metabolite(compound) name" + Utils.bcolors.ENDC)

# parameterization
if len(sys.argv) > 2:
	sys_args = sys.argv[2]
	combinations = ['','-msp', '-mps', '-smp', '-spm', '-pms', '-psm', '-sp', '-ps']
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
	elif sys_args in ['--show-result', '--download-tsv']:
		if sys_args == '--show-result':
			show_result = True
		elif sys_args == '--download-tsv':
			down_tsv = True 
	else:
		raise Exception(Utils.bcolors.FAIL + "Please try again with right parameters" + Utils.bcolors.ENDC)
elif len(sys.argv) > 3:
	sys_args = sys.argv[3]
	if sys_args == '--download-tsv':
		down_tsv = True
	else:
		down_tsv = False


if down_tsv:
	download_names_tsv()

if show_result:
	os.system("python prepare_output.py '{}'".format(metabolite_name))
	sys.exit(1)

# Run utils.py to get data
with open('output/{}.json'.format(metabolite_name), 'w') as fp:
	json.dump(Utils(metabolite_name, synonym=inc_syn, precursor=inc_prec).result, fp, indent=4)

# Remove unnecessary files
os.system("rm -rf output/*.txt")

# Create HTML and TSV file for displaying data from JSON
os.system("python prepare_output.py '{}'".format(metabolite_name))
