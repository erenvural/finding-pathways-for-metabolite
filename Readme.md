# Finding Pathways for a given metabolite

## Project Details
__Question__: Given a metabolite can you find the pathways/network it and its immediate precursors
exist?
* Metabolite can be by name, formula, smiles code. (Chebi, PubChem etc. identifier) (Query expansion)
* Pathway could be from any database (Wikipathways, Reactome etc.).
* Use pathway, reaction, chemical compound/human metabolite databases.

##  Steps
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
	* Restfull API: "http://rest.kegg.jp/find/rn/glutamate" or "http://rest.kegg.jp/find/reaction/glutamate": it gives us a flat file.

- For Pathway we search trough the Reactome Pathway, KEGG Pathway, Wikipathway, and return the result set.
	* Link (aspirin) => http://www.reactome.org/content/query?q=aspirin&species=Homo+sapiens&species=Entries+without+species&types=Pathway&cluster=true


## Questions:
- to prune we need a list which contains: `CO2`, `H2O`: use Frequency to detect those words (stopwords detecting like method).

## Dependicies:
-	curl 7.47.0
- Python2.7
- Java (JDK path must be given at line 6)(Tried with jdk1.8.0_101)
- Perl 5.22

## Usage:
- to most common run (include metabolite name, synonyms and precursors):

	``` ./scr.py $metabolite_name ```
	or
	``` ./scr.py $metabolite_name -msp ```

- to only search for metabolite name (exclude synonyms, precursors):

	``` ./scr.py $metabolite name -m ```

- to only search for metabolite name and synonyms (exclude precursors):

	``` ./scr.py $metabolite name -ms ```
	
---
---
#### Helper Command
```
curl http://rest.kegg.jp/find/rn/glutamate | perl -e 'while(<>){ if ($_ =~ /^rn\:R[0-9]*\s*(.*)\<\=\>/){ if ($1 !~ /{}/i) { print "$1\n" }  }}' > glutamate.clean.txt
```
---
---
### The requierement for Presentation:

#### 1. Describe your problem/research question.

__Question__: Given a metabolite can you find the pathways/network it and its immediate precursors exist?
	- Metabolite can be by name, formula, smiles code. (Chebi, PubChem etc. identifier) (Query expansion)
	- Pathway could be from any database (Wikipathways, Reactome etc.).
	- Use pathway, reaction, chemical compound/human metabolite databases.

#### 2. List team members and  their roles.

| Team Members            | Github Accounts                           |
|-------------------------|-------------------------------------------|
| Eren VURAL              |[erenvural](https://github.com/erenvural)  |
| Mahmut KOÇAKER          |[mkocaker06](https://github.com/mkocaker06)|
| Muhammed Olcay TERCANLI |[molcay](https://github.com/molcay)        |

#### 3. Describe the method employed. Be specific on steps and name of tools/databases.
* We get the metabolite name from user.
* We search the metabolite on __CheBI__ and get the results for a metabolite(a query can match with multiple entry on __CheBI__).
* We visit every matches pages and getting the synonyms for the given metabolite.
* We search through the __KEGG Reaction__ and getting precursor for the given metabolite and its synonyms.
* When collection of all synonyms and precursors have done, we search for pathways with metabolite name, synonyms and precursors.
* As a result we list the pathways from __WikiPathways__, __Reactome__ etc.:

	| METABOLITE_NAME		| Metabolite(M)/Synonyms(S)/Precursor(P)		| PATHWAYS 		        |
	|-----------------------|-----------------------------------------------|-----------------------|
	| Aspirin 				| M 											| URL(wikipathways/asd) |

#### 4. Provide example codes and scripts and describe how you organized them.

#### 5. Run a demo with a described example scenario

#### 6.  Provide pointers to source code (GitHub/Attassian BitBucket/Zip file etc.)

#### 7. Presentation
* link : https://prezi.com/mhq98qbpnz5_/finding-pathways-for-metabolite/
