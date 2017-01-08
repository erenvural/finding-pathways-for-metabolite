#!-*- coding: utf-8 -*-
import urllib2, json, os, csv
import xml.etree.ElementTree as ET


class Utils:

	class bcolors: # console print coloring
		HEADER = '\033[95m'
		OKBLUE = '\033[94m'
		OKGREEN = '\033[92m'
		WARNING = '\033[93m'
		FAIL = '\033[91m'
		ENDC = '\033[0m'
		BOLD = '\033[1m'
		UNDERLINE = '\033[4m'

	with open('script.config', 'r') as fp:
		CONFIG = json.load(fp)
	__JAVA_HOME__ = CONFIG['java_bin']

	COMMON_PRECURSORS = ["ATP", "H2O", 'CO2', 'CO']

	__XML_IDENTIFIER_FOR_CHEBI__ = "{http://www.ebi.ac.uk/webservices/chebi}" # self.__XML_IDENTIFIER_FOR_CHEBI__
	__XML_IDENTIFIER_FOR_SOAP_ENVELOPE__ = "{http://schemas.xmlsoap.org/soap/envelope/}"

	# SEARCH_URL = "https://www.ebi.ac.uk/chebi/advancedSearchFT.do?queryBean.stars=2&searchString="
	COMPOUND_URL = "https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:"
	CHEBI_XML_URL = "https://www.ebi.ac.uk/webservices/chebi/2.0/test/getCompleteEntity?chebiId="
	KEGG_REACTION_URL = "http://rest.kegg.jp/find/rn/"
	WPW_XML_URL = "http://webservice.wikipathways.org/findPathwaysByText?query="
	REACTOME_SEARCH_URL = "http://www.reactome.org/content/query?types=Pathway&cluster=true&page=1&q="
	REACTOME_PATHWAY_URL = "http://reactome.org/PathwayBrowser/#/"

	def __init__(self, metabolite, synonym=True, precursor=True):
		self.metabolite = metabolite # came from tsv depends on user parameter
		self.compound_id = self.get_compound_id(self.metabolite) # came from tsv
		self.result = {'name': self.metabolite, 'chebiID': self.compound_id}
		if synonym:
			self.get_synonyms()
		if precursor:
			if synonym:
				self.get_precursors([self.metabolite] + self.result['synonyms'])
			else:
				self.get_precursors([self.metabolite])
		self.get_pathways()

	def get_compound_id(self, search_for):
		result = ""
		with open(self.CONFIG['names_tsv']) as tsvfile:
			tsvreader = csv.reader(tsvfile, delimiter="\t")
			for row in tsvreader:
				if (row[4].lower() == search_for) and (row[2] == "NAME"):
					result = row[1]

		return result

	def get_synonyms(self):
		xml_file_url = self.CHEBI_XML_URL + self.compound_id
		req = urllib2.Request(xml_file_url)
		response = urllib2.urlopen(req)
		xml_page = response.read()

		root = ET.fromstring(xml_page)
		body = root.find("{0}Body".format(self.__XML_IDENTIFIER_FOR_SOAP_ENVELOPE__))
		getCompleteEntityResponse = body.find("{0}getCompleteEntityResponse".format(self.__XML_IDENTIFIER_FOR_CHEBI__))
		for comp in getCompleteEntityResponse.findall("{0}return".format(self.__XML_IDENTIFIER_FOR_CHEBI__)):
			compound_name = comp.find("{0}chebiAsciiName".format(self.__XML_IDENTIFIER_FOR_CHEBI__)).text
			synonyms = comp.findall("{0}Synonyms".format(self.__XML_IDENTIFIER_FOR_CHEBI__))
			synonyms_list = []

			for syn in synonyms:
				synonym_name = syn.find("{0}data".format(self.__XML_IDENTIFIER_FOR_CHEBI__)).text
				if synonym_name != self.metabolite:
					synonyms_list.append(synonym_name)
		# print(synonyms_list)
		# if self.metabolite.lower() in [s.lower() for s in synonyms_list]:
		self.result['synonyms'] = synonyms_list

	def get_precursors(self, search_list):
		# print(search_list)
		delete_list = [H2O, ATP, UTP]
		result = []
		for (i, search_term) in enumerate(search_list):
			# print(i, search_term)
			print("Getting Precursors for: " + search_term)

			reaction_url = self.KEGG_REACTION_URL + search_term
			print("HTTP Request for: " + reaction_url)
			command = """curl -s "%s" | perl -e 'while(<>){ if ($_ =~ /^rn\:R[0-9]*\s*(.*)\<\=\>/){ if ($1 !~ /%s/i) { print "$1\n" }  }}' """ % (reaction_url, search_term)
			precursors_candidates = os.popen(command).read()

			precursors_fc = self.get_precursor_list(precursors_candidates)
			print("# of precursors found for {}: {}".format(search_term, len(precursors_fc)))
			flag = False
			for delete_prec in delete_list:
				if delete_prec.find(search_term) =! -1:
					flag = True

			if flag:
				if i == 0: # Metabolite itself
					for prec in precursors_fc:
						precursor = {
							'parent': {'type': "M", 'name': search_term},
							'name': prec
							}
						result.append(precursor)
				else:
					for prec in precursors_fc:
						precursor = {
							'parent': {'type': "S", 'name': search_term},
							'name': prec
							}
						result.append(precursor)
			else:
				pass
		# print(result)
		self.result['precursors'] = result
		print("Getting Precursors done")

	def get_precursor_list(self, precursors_candidates):
		lines = precursors_candidates.split("\n")
		precursors = []
		for line in lines:
			if (line.find(";") != -1):
				line = line[(line.find(";") + 2):]
			for precursor in [f.strip() for f in line.split(" + ") if f != ""]:
				if precursor not in precursors:
					precursors.append(precursor)
		return precursors

	def get_pathways(self):
		self.result['pathways'] = { 'reactome': self.get_pathways_from_reactome(self.metabolite), 'wikipathways': self.get_pathways_from_wikipathways(self.metabolite)}

	def get_pathways_from_reactome(self, metabolite_name):
		html_page_url = self.REACTOME_SEARCH_URL + metabolite_name
		command = """curl -s "%s" | perl -e '@results = []; while(<>) { if($_ =~ /\<a\shref\=\"\.\/detail\/(.*)\d\"(.*)\<\/a\>/) { $id = $1; $name = $2; $name =~ s/.*\>//; print "$name => $id\n"; } }' """ % html_page_url
		pw_output = os.popen(command).read()
		pws = [i for i in pw_output.split("\n") if i != '']
		reactome_pathway_list = []
		for p in pws:
			pathway = {}
			pathway['name'] = p.split(" => ")[0]
			pathway['url'] = self.REACTOME_PATHWAY_URL + p.split(" => ")[1]
			reactome_pathway_list.append(pathway)

		return reactome_pathway_list

	def get_pathways_from_wikipathways(self, metabolite_name):
		# http://webservice.wikipathways.org/findPathwaysByText?query=glutamate
		xml_file_url = self.WPW_XML_URL + metabolite_name
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
