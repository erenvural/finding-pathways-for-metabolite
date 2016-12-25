#!/usr/bin/python
import os, sys, re, json, urllib2, getopt
import xml.etree.ElementTree as ET

# Environment variable
__JAVA_HOME__ = "/opt/java/jdk1.8.0_101/bin/"

__GETPRECURSOR_JAVA__ = "GetPrecursors"

__XML_IDENTIFIER_FOR_CHEBI__ = "{http://www.ebi.ac.uk/webservices/chebi}"
__XML_IDENTIFIER_FOR_SOAP_ENVELOPE__ = "{http://schemas.xmlsoap.org/soap/envelope/}"

SEARCH_URL = "https://www.ebi.ac.uk/chebi/advancedSearchFT.do?queryBean.stars=2&searchString="
COMPOUND_URL = "https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:"
CHEBI_XML_URL = "https://www.ebi.ac.uk/webservices/chebi/2.0/test/getCompleteEntity?chebiId="
WPW_XML_URL = "http://webservice.wikipathways.org/findPathwaysByText?query="
REACTOME_SEARCH_URL = "http://www.reactome.org/content/query?types=Pathway&cluster=true&page=1&q="
REACTOME_PATHWAY_URL = "http://reactome.org/PathwayBrowser/#/"


def getCompounds(metabolite_name):
	fsp_url = SEARCH_URL + metabolite_name.replace(" ", "+") # The first search page
	req = urllib2.Request(fsp_url)
	response = urllib2.urlopen(req)
	fsp_content = response.read().replace("\n", "")
	session_id = ""
	for s in re.finditer(r'jsessionid\=(.*?)\"', fsp_content):
		session_id = s.group(0).replace('"', "")
	compound_id_list = []

	for m in re.finditer(r'(?<=CHEBI:)\d+', fsp_content):
		if m.group(0) not in compound_id_list:
			compound_id_list.append(m.group(0))
	return compound_id_list

def getSynonyms(c_id):
	xml_file_url = CHEBI_XML_URL + c_id
	req = urllib2.Request(xml_file_url)
	response = urllib2.urlopen(req)
	xml_page = response.read()

	root = ET.fromstring(xml_page)
	body = root.find("{0}Body".format(__XML_IDENTIFIER_FOR_SOAP_ENVELOPE__))
	getCompleteEntityResponse = body.find("{0}getCompleteEntityResponse".format(__XML_IDENTIFIER_FOR_CHEBI__))
	for comp in getCompleteEntityResponse.findall("{0}return".format(__XML_IDENTIFIER_FOR_CHEBI__)):
		compound_name = comp.find("{0}chebiAsciiName".format(__XML_IDENTIFIER_FOR_CHEBI__)).text
		synonyms = comp.findall("{0}Synonyms".format(__XML_IDENTIFIER_FOR_CHEBI__))
		synonyms_list = []
		
		for syn in synonyms:
			synonym_name = syn.find("{0}data".format(__XML_IDENTIFIER_FOR_CHEBI__)).text
			synonyms_list.append(synonym_name)
	# print(synonyms_list)
	if metabolite_name.lower() in [s.lower() for s in synonyms_list]:
		# print(compound_name)
		compound = {
			'compound_id': c_id,
			'compound_name': compound_name.replace(" ", ""),
			'synonyms': synonyms_list
		}
		return compound


def getPrecursors(metabolite_name):
	command = """curl -s http://rest.kegg.jp/find/rn/%s | perl -e 'while(<>){ if ($_ =~ /^rn\:R[0-9]*\s*(.*)\<\=\>/){ if ($1 !~ /%s/i) { print "$1\\n" }  }}' > %s.clean.txt""" % (metabolite_name, metabolite_name, metabolite_name)
	os.system(command)

	os.system("{0}javac {1}.java".format(__JAVA_HOME__, __GETPRECURSOR_JAVA__)) # to compile the script for GetPrecursors
	command = "{0}java {1} {2}".format(__JAVA_HOME__, __GETPRECURSOR_JAVA__, metabolite_name)
	os.system(command)
	"""# os.system("mkdir temp")
	# os.system("rm -rf temp")
	"""
	precursors_fc = open("{0}.precursors.txt".format(metabolite_name), "r").readlines()

	return [precursor.replace("\n", "") for precursor in precursors_fc]


def getPathwaysFromWikiPathways(metabolite_name):
	# http://webservice.wikipathways.org/findPathwaysByText?query=glutamate
	xml_file_url = WPW_XML_URL + metabolite_name
	req = urllib2.Request(xml_file_url)
	response = urllib2.urlopen(req)
	xml_page = response.read()
	wpw_pathways_list = []

	root = ET.fromstring(xml_page)
	for result in root:
		wpw_url = result.find("{0}url".format("{http://www.wikipathways.org/webservice}")).text
		wpw_name = result.find("{0}name".format("{http://www.wikipathways.org/webservice}")).text
		pathway = {'name': wpw_name, 'url': wpw_url}
		wpw_pathways_list.append(pathway)

	return wpw_pathways_list

def getPathwaysFromReactome(metabolite_name):
	html_page_url = REACTOME_SEARCH_URL + metabolite_name
	command = """curl -s "%s" | perl -e '@results = []; while(<>) { if($_ =~ /\<a\shref\=\"\.\/detail\/(.*)\d\"(.*)\<\/a\>/) { $id = $1; $name = $2; $name =~ s/.*\>//; print "$name => $id\n"; } }' """ % html_page_url
	pw_output = os.popen(command).read()
	pws = [i for i in pw_output.split("\n") if i != '']
	reactome_pathway_list = []
	for p in pws:
		pathway = {}
		pathway['name'] = p.split(" => ")[0]
		pathway['url'] = REACTOME_PATHWAY_URL + p.split(" => ")[1]
		reactome_pathway_list.append(pathway)

	return reactome_pathway_list

# metabolite_name = "aspirin"
metabolite_name = sys.argv[1]

compound_id_list = getCompounds(metabolite_name)

result = { metabolite_name : [] }
for c_id in compound_id_list:

	compound = getSynonyms(c_id)
	if compound:
		# !!!! for now getting precursors only for metabolite name
		compound['precursors'] = getPrecursors("glutamate") 
		# compound['precursors'] = [getPrecursors(c) for c in synonyms_list]]
		# print(compound)
		result[metabolite_name].append(compound)
		result['reactome'] = getPathwaysFromReactome(metabolite_name)
		result['wikipathways'] = getPathwaysFromWikiPathways(metabolite_name)

with open(metabolite_name + '.json', 'w') as fp:
		json.dump(result, fp, indent=4)

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
