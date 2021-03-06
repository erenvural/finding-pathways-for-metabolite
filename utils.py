#!-*- coding: utf-8 -*-
import os, sys, urllib2, json, csv
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

	TSV_FILE = CONFIG['names_tsv']

	COMMON_PRECURSORS = ["ATP", "H2O", 'CO2', 'CO']

	INDENT = 2

	__XML_IDENTIFIER_FOR_CHEBI__ = "{http://www.ebi.ac.uk/webservices/chebi}" # self.__XML_IDENTIFIER_FOR_CHEBI__
	__XML_IDENTIFIER_FOR_SOAP_ENVELOPE__ = "{http://schemas.xmlsoap.org/soap/envelope/}"

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
		if synonym and not precursor:
			self.println("We will search pathways for: {} and its synonyms (excluding precursors)...".format(metabolite), color=self.bcolors.OKGREEN)
			self.get_synonyms()
			pathway_getting_list = [self.metabolite] + self.result['synonyms']
		elif synonym and precursor:
			self.println("We will search pathways for: {}, its synonyms and its precursors...".format(metabolite), color=self.bcolors.OKGREEN)
			self.get_synonyms()
			self.get_precursors([self.metabolite] + self.result['synonyms'])
			pathway_getting_list = [self.metabolite] + self.result['synonyms'] + self.result['precursors']
		elif not synonym and precursor:
			self.println("We will search pathways for: {} and its precursors (excluding synonyms)...".format(metabolite), color=self.bcolors.OKGREEN)
			self.get_precursors([self.metabolite])
			pathway_getting_list = [self.metabolite] + self.result['precursors']
		elif not synonym and not precursor:
			self.println("We will search pathways for: {} (exclude synonyms and precursors)...".format(metabolite), color=self.bcolors.OKGREEN)
			pathway_getting_list = [self.metabolite]
		else:
			self.println("Parameters not recognized", color=self.bcolors.FAIL)
			sys.exit(1)
		self.get_pathways(pathway_getting_list)


	def get_compound_id(self, search_for):
		result = ""
		with open(self.TSV_FILE) as tsvfile:
			tsvreader = csv.reader(tsvfile, delimiter="\t")
			for row in tsvreader:
				if (row[4].lower() == search_for) and (row[2] == "NAME"):
					result = row[1]

		return result

	def get_synonyms(self):
		self.println("Getting synonyms for: {} (CheBI ID: {})".format(self.metabolite, self.compound_id), indent=self.INDENT, color=self.bcolors.BOLD+self.bcolors.OKBLUE)
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
		
		self.println("# of synonyms found for {}: {}".format(self.metabolite, len(synonyms_list)), indent=self.INDENT * 2, color=self.bcolors.OKBLUE)
		self.println("Getting Synonyms process done", indent=self.INDENT * 2, color=self.bcolors.OKBLUE)
		self.result['synonyms'] = synonyms_list

	def get_precursors(self, search_list):
		result = []
		for (i, search_term) in enumerate(search_list):
			self.println("Getting Precursors for: {}".format(search_term), indent=self.INDENT, color=self.bcolors.BOLD+self.bcolors.OKBLUE)

			reaction_url = self.KEGG_REACTION_URL + search_term

			command = """curl -s "%s" | perl -e 'while(<>){ if ($_ =~ /^rn\:R[0-9]*\s*(.*)\<\=\>/){ if ($1 !~ /%s/i) { print "$1\n" }  }}' """ % (reaction_url, search_term)
			precursors_candidates = os.popen(command).read()

			precursors_fc = self.get_precursor_list(precursors_candidates)
			self.println("# of precursors found for {}: {}".format(search_term, len(precursors_fc)), indent=self.INDENT * 2, color=self.bcolors.OKBLUE)

			if i == 0: # Metabolite itself
				for prec in precursors_fc:
					if not self.is_common(prec):
						precursor = {
							'parent': {'type': "M", 'name': search_term},
							'name': prec
							}
						result.append(precursor)
			else:
				for prec in precursors_fc:
					if not self.is_common(prec):
						precursor = {
							'parent': {'type': "S", 'name': search_term},
							'name': prec
							}
						result.append(precursor)

		# self.result['precursors'] = result[:3] # for debug uncomment this and comment the previous line
		self.println("Getting Precursors process done", indent=self.INDENT * 2, color=self.bcolors.OKBLUE)
		self.result['precursors'] = result


	def is_common(self, precursor):
		for c_pre in self.COMMON_PRECURSORS:
			if precursor.find(c_pre) != -1:
				return True
		return False

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

	def get_pathways(self, search_list):
		result = {'reactome': [], 'wikipathways': []}
		for (i, search_term) in enumerate(search_list):
			if i == 0: # metabolite itself
				self.println("Getting Pathways for: {}".format(search_term), indent=self.INDENT, color=self.bcolors.BOLD+self.bcolors.OKBLUE)
				parent = { 'type': "M", 'name': search_term }
				for pathway in self.get_pathways_from_reactome(search_term, parent):
						result['reactome'].append(pathway)
				for pathway in self.get_pathways_from_wikipathways(search_term, parent):
						result['wikipathways'].append(pathway)
			else:
				if type(search_term) == str: # synonyms
					self.println("Getting Pathways for: {}".format(search_term), indent=self.INDENT, color=self.bcolors.BOLD+self.bcolors.OKBLUE)
					parent = { 'type': "S", 'name': search_term }
					for pathway in self.get_pathways_from_reactome(search_term, parent):
						result['reactome'].append(pathway)
					for pathway in self.get_pathways_from_wikipathways(search_term, parent):
						result['wikipathways'].append(pathway)
				elif type(search_term) == dict: # precursors
					self.println("Getting Pathways for: {}".format(search_term['name']), indent=self.INDENT, color=self.bcolors.BOLD+self.bcolors.OKBLUE)
					parent = search_term
					for pathway in self.get_pathways_from_reactome(search_term['name'], parent):
						result['reactome'].append(pathway)
					for pathway in self.get_pathways_from_wikipathways(search_term['name'], parent):
						result['wikipathways'].append(pathway)
				else:
					self.println("Someting went wrong while getting pathways", indent=self.INDENT, color=self.bcolors.BOLD+self.bcolors.FAIL)
					sys.exit(1)

		self.println("#"*60, indent=self.INDENT, color=self.bcolors.OKBLUE)
		self.println("The total # of pathways for {}: {}".format(self.metabolite, len(result['reactome']) + len(result['wikipathways'])), indent=self.INDENT, color=self.bcolors.OKBLUE)
		self.println("Getting Pathways process done", indent=self.INDENT, color=self.bcolors.OKBLUE)
		self.result['pathways'] = result

	def get_pathways_from_reactome(self, search_term, parent):
		html_page_url = self.REACTOME_SEARCH_URL + search_term
		command = """curl -s "%s" | perl -e '@results = []; while(<>) { if($_ =~ /\<a\shref\=\"\.\/detail\/(.*)\d\"(.*)\<\/a\>/) { $id = $1; $name = $2; $name =~ s/.*\>//; print "$name => $id\n"; } }' """ % html_page_url
		pw_output = os.popen(command).read()
		pws = [i for i in pw_output.split("\n") if i != '']
		reactome_pathway_list = []
		for p in pws:
			pathway = {'parent': parent}
			pathway['name'] = p.split(" => ")[0]
			pathway['url'] = self.REACTOME_PATHWAY_URL + p.split(" => ")[1]
			reactome_pathway_list.append(pathway)

		return reactome_pathway_list

	def get_pathways_from_wikipathways(self, search_term, parent):
		xml_file_url = self.WPW_XML_URL + search_term
		req = urllib2.Request(xml_file_url)
		response = urllib2.urlopen(req)
		xml_page = response.read()
		wpw_pathways_list = []

		root = ET.fromstring(xml_page)
		for result in root:
			wpw_url = result.find("{0}url".format("{http://www.wikipathways.org/webservice}")).text
			wpw_name = result.find("{0}name".format("{http://www.wikipathways.org/webservice}")).text
			pathway = {'parent': parent,'name': wpw_name, 'url': wpw_url}
			wpw_pathways_list.append(pathway)

		return wpw_pathways_list

	def println(self, string, indent=0, color=""):
		print('{0}{1}{2}{3}'.format(" " * indent, color, string, self.bcolors.ENDC))