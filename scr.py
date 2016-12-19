#!/usr/bin/python

import os, sys, re, json, urllib2
import xml.etree.ElementTree as ET

# Environment variable
__JAVA_HOME__ = "/opt/java/jdk1.8.0_111/bin/"

__GETPRECURSOR_JAVA__ = "GetPrecursors"

__XML_IDENTIFIER_FOR_CHEBI__ = "{http://www.ebi.ac.uk/webservices/chebi}"
__XML_IDENTIFIER_FOR_SOAP_ENVELOPE__ = "{http://schemas.xmlsoap.org/soap/envelope/}"

SEARCH_URL = "https://www.ebi.ac.uk/chebi/advancedSearchFT.do?queryBean.stars=2&searchString="
COMPOUND_URL = "https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:"
XML_URL = "https://www.ebi.ac.uk/webservices/chebi/2.0/test/getCompleteEntity?chebiId="


def getCompounds(metabolite_name):
	fsp_url = SEARCH_URL + metabolite_name.replace(" ", "+") # The first search page
	req = urllib2.Request(fsp_url)
	response = urllib2.urlopen(req)
	fsp_content = response.read().replace("\n", "")

	compound_id_list = []
	for m in re.finditer(r'(?<=CHEBI:)\d+', fsp_content):
		if m.group(0) not in compound_id_list:
			compound_id_list.append(m.group(0))
	return compound_id_list


def getSynonyms(c_id):
	xml_file_url = XML_URL + c_id
	req = urllib2.Request(xml_file_url)
	response = urllib2.urlopen(req)
	xml_page = response.read()

	root = ET.fromstring(xml_page)
	body = root.find("{}Body".format(__XML_IDENTIFIER_FOR_SOAP_ENVELOPE__))
	getCompleteEntityResponse = body.find("{0}getCompleteEntityResponse".format(__XML_IDENTIFIER_FOR_CHEBI__))
	for comp in getCompleteEntityResponse.findall("{0}return".format(__XML_IDENTIFIER_FOR_CHEBI__)):
		compound_name = comp.find("{0}chebiAsciiName".format(__XML_IDENTIFIER_FOR_CHEBI__)).text
		synonyms = comp.findall("{0}Synonyms".format(__XML_IDENTIFIER_FOR_CHEBI__))
		synonyms_list = []
		for syn in synonyms:
			synonym_name = syn.find("{0}data".format(__XML_IDENTIFIER_FOR_CHEBI__)).text
			synonyms_list.append(synonym_name)
	# print(synonyms_list)
	compound = {
		'compound_id': c_id,
		'compound_name': compound_name.replace(" ", ""),
		'synonyms': synonyms_list
	}
	return compound


def getPrecursors(metabolite_name):
	command = """curl http://rest.kegg.jp/find/rn/%s | perl -e 'while(<>){ if ($_ =~ /^rn\:R[0-9]*\s*(.*)\<\=\>/){ if ($1 !~ /%s/i) { print "$1\\n" }  }}' > %s.clean.txt""" % (metabolite_name, metabolite_name, metabolite_name)
	os.system(command)

	os.system("{0}javac {}.java".format(__JAVA_HOME__, __GETPRECURSOR_JAVA__)) # to compile the script for GetPrecursors
	command = "{0}java {1} {2}".format(__JAVA_HOME__, __GETPRECURSOR_JAVA__, metabolite_name)
	os.system(command)
	"""# os.system("mkdir temp")
	# os.system("rm -rf temp")
	"""
	precursors_fc = open("{}.precursors.txt".format(metabolite_name), "r").readlines()

	return [precursor.replace("\n", "") for precursor in precursors_fc]


def parseCheBI():
	pass

def parsePrecursor():
	pass

metabolite_name = "aspirin"
# metabolite_name = sys.ARGV[1]

compound_id_list = getCompounds(metabolite_name)

result = { metabolite_name : [] }
for c_id in compound_id_list:
	
	compound = getSynonyms(c_id)

	compound['precursors'] = getPrecursors("glutamate")

	print(compound)
	# compound['precursors'] = [getPrecursors(c) for c in synonyms_list]]
	
	result[metabolite_name].append(compound)

"""
with open(metabolite_name + '.json', 'w') as fp:
		json.dump(result, fp, indent=4)
"""

# 

"""
http://rest.kegg.jp/find/rn/glutamate
or 
http://rest.kegg.jp/find/reaction/glutamate


curl http://rest.kegg.jp/find/rn/glutamate | perl -e 'while(<>){ if ($_ =~ /^rn\:R[0-9]*\s*(.*)\<\=\>/){ if ($1 !~ /{}/i) { print "$1\n" }  }}' > glutamate.clean.txt
"""