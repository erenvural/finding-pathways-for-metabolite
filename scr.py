#!/usr/bin/python
"""
from Bio.Seq import Seq

#create a sequence object
my_seq = Seq('CATGTAGACTAG')

#print out some details about it
print 'seq %s is %i bases long' % (my_seq, len(my_seq))
print 'reverse complement is %s' % my_seq.reverse_complement()
print 'protein translation is %s' % my_seq.translate()

"""
import os, re, json, urllib2
import xml.etree.ElementTree as ET

SEARCH_URL = "https://www.ebi.ac.uk/chebi/advancedSearchFT.do?queryBean.stars=2&searchString="

COMPOUND_URL = "https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:"

XML_URL = "https://www.ebi.ac.uk/webservices/chebi/2.0/test/getCompleteEntity?chebiId="


# metabolite_name = str(raw_input("Give a metabolite name: "))
metabolite_name = "aspirin"


fsp_url = SEARCH_URL + metabolite_name.replace(" ", "+")
req = urllib2.Request(fsp_url)
response = urllib2.urlopen(req)
the_fsp = response.read().replace("\n", "")

compound_id_list = []
for m in re.finditer(r'(?<=CHEBI:)\d+', the_fsp):
	if m.group(0) not in compound_id_list:
		compound_id_list.append(m.group(0))

result = { metabolite_name : [] }
for c_id in compound_id_list:
	c_url = COMPOUND_URL + c_id

	xml_file_url = XML_URL + c_id
	req = urllib2.Request(xml_file_url)
	response = urllib2.urlopen(req)
	the_page = response.read()

	root = ET.fromstring(the_page)
	body = root.find("{http://schemas.xmlsoap.org/soap/envelope/}Body")
	getCompleteEntityResponse = body.find("{http://www.ebi.ac.uk/webservices/chebi}getCompleteEntityResponse")
	for comp in getCompleteEntityResponse.findall("{http://www.ebi.ac.uk/webservices/chebi}return"):
		compound_name = comp.find("{http://www.ebi.ac.uk/webservices/chebi}chebiAsciiName").text
		synonyms = comp.findall("{http://www.ebi.ac.uk/webservices/chebi}Synonyms")
		synonyms_list = []
		for syn in synonyms:
			synonym_name = syn.find("{http://www.ebi.ac.uk/webservices/chebi}data").text
			synonyms_list.append(synonym_name)
	# print(synonyms_list)
	compound = {
		'compound_id': c_id,
		'compound_name': compound_name.replace(" ", ""),
		'synonyms': synonyms_list
	}
	result[metabolite_name].append(compound)
	# print(result)

with open(metabolite_name + '.json', 'w') as fp:
		json.dump(result, fp)
