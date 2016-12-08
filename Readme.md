# Get Pathways

- Take a metabolite name from user (e.g: _`aspirin`_):

- Getting search result for metabolite from CheBI:
	* for first search: "https://www.ebi.ac.uk/chebi/advancedSearchFT.do?queryBean.stars=2&searchString=aspirin"

- Getting synonyms for every search result from CheBI and store the synonyms in a file called `metabolite_name.json` (e.g: _`aspirin.json`_):
	* for metabolite details: "https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:15365"
	* for metabolite synonyms: "https://www.ebi.ac.uk/webservices/chebi/2.0/test/getCompleteEntity?chebiId=15365"
	* __`metabolite_name.json`__ (e.g: _`aspirin.json`_):
	```
	{
		"aspirin" : [
			{
				'chebi_id': 31318,
				'chebi_name': Bufferin,
				'synonyms': ['Aspirin softam', 'Bufferin']
			},
			{
				'chebi_id': 15365,
				'chebi_name': "acetylsalicylic acid",
				'synonyms': ['2-(ACETYLOXY)BENZOIC ACID', '2-Acetoxybenzenecarboxylic acid', '2-acetoxybenzoic acid', ...]
			}
		]
	}
	```

- For All keywords (metabolite & synonyms) we search for reactions from KEGG Reactions.(We prune the data which contains the keyword within right side)

	* Link (glutamate)=> http://www.kegg.jp/dbget-bin/www_bfind_sub?dbkey=reaction&keywords=glutamate&mode=bfind&max_hit=nolimit

- For Pathway we search trough the Reactome Pathway, KEGG Pathway, Wikipathway, and return the result set.

	* Link (aspirin) => http://www.reactome.org/content/query?q=aspirin&species=Homo+sapiens&species=Entries+without+species&types=Pathway&cluster=true





### Questions:
- to prune we need a list which contains: `CO2`, `H2O`