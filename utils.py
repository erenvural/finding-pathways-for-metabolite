import urllib2, json, os, csv
import xml.etree.ElementTree as ET


class Utils:

	with open('script.config', 'r') as fp:
		CONFIG = json.load(fp)
	__JAVA_HOME__ = CONFIG['java_bin']
	
	__GETPRECURSOR_JAVA__ = "GetPrecursors"
	
	__XML_IDENTIFIER_FOR_CHEBI__ = "{http://www.ebi.ac.uk/webservices/chebi}" # self.__XML_IDENTIFIER_FOR_CHEBI__
	__XML_IDENTIFIER_FOR_SOAP_ENVELOPE__ = "{http://schemas.xmlsoap.org/soap/envelope/}"
	
	SEARCH_URL = "https://www.ebi.ac.uk/chebi/advancedSearchFT.do?queryBean.stars=2&searchString="
	COMPOUND_URL = "https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:"
	CHEBI_XML_URL = "https://www.ebi.ac.uk/webservices/chebi/2.0/test/getCompleteEntity?chebiId="
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
			self.get_precursors()
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
				synonyms_list.append(synonym_name)
		# print(synonyms_list)
		if self.metabolite.lower() in [s.lower() for s in synonyms_list]:
			# print(compound_name)
			"""
			compound = {
				'compound_id': self.compound_id,
				'compound_name': compound_name.replace(" ", ""),
				'synonyms': synonyms_list
			}
			print(compound)
			return compound
			"""
			self.result['synonyms'] = synonyms_list

	def get_precursors(self):
		# return
		command = """curl -s http://rest.kegg.jp/find/rn/%s | perl -e 'while(<>){ if ($_ =~ /^rn\:R[0-9]*\s*(.*)\<\=\>/){ if ($1 !~ /%s/i) { print "$1\\n" }  }}' > output/%s.clean.txt""" % (self.metabolite, self.metabolite, self.metabolite)
		os.system(command)
	

		os.system("{0}javac {1}.java".format(self.__JAVA_HOME__, self.__GETPRECURSOR_JAVA__)) # to compile the script for GetPrecursors
		command = "{0}java {1} {2}".format(self.__JAVA_HOME__, self.__GETPRECURSOR_JAVA__, self.metabolite)
		os.system(command)
		"""
			# os.system("mkdir temp")
			# os.system("rm -rf temp")
		"""
		precursors_fc = open("output/{0}.precursors.txt".format(self.metabolite), "r").readlines()
		
		self.result['precursors'] = [precursor.replace("\n", "") for precursor in precursors_fc]

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


	