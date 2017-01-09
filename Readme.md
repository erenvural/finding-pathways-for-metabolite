# Finding Pathways for a given metabolite

## Project Details
__Question__: Given a metabolite can you find the pathways/network it and its immediate precursors
exist?
* Metabolite can be by name, formula, smiles code. (ChEBI, PubChem etc. identifier) (Query expansion)
* Pathway could be from any database (Wikipathways, Reactome etc.).
* Use pathway, reaction, chemical compound/human metabolite databases.

##  Steps
- Taking a metabolite name from user (e.g: _`aspirin`_)
- Getting search result for metabolite from names.tsv which download from ChEBI
- Getting synonyms for every search result from CheBI and store the synonyms in a file called `metabolite_name.json` (e.g: _`aspirin.json`_):
- For All keywords (metabolite & synonyms) we search for reactions from KEGG Reactions.(We prune the data which contains the keyword within right side)
- For Pathway we search trough the Reactome Pathway, KEGG Pathway, Wikipathway, and return the result set.

## Questions:
- to prune we need a list which contains: `CO2`, `H2O`: use Frequency to detect those words (stopwords detecting like method).

## Dependicies:
- Python 2.7
- Perl 5.22
- Curl 7.47.0
- Wget 1.17.1
- gzip 1.6

## Usage:

> In any parameter there is no rule for order. (e.g: `-msp` can be `-spm` or `-psm`)

- to most common run (include metabolite name, synonyms and precursors):

	``` ./scr.py $metabolite_name ```
	
	or
	
	``` ./scr.py $metabolite_name -msp ``` 

- to only search for metabolite name (exclude synonyms, precursors):

	``` ./scr.py $metabolite name -m ```

- to only search for metabolite name and synonyms (exclude precursors):

	``` ./scr.py $metabolite name -s ```

	or

	``` ./scr.py $metabolite name -ms ```

- to only search for metabolite name and precursors (exclude precursors):

	``` ./scr.py $metabolite_name -p ```

	or

	``` ./scr.py $metabolite name -mp ```
	
---
### Presentation
* link : https://prezi.com/mhq98qbpnz5_/finding-pathways-for-metabolite/

### Team Members
| Team Members            | Github Accounts                           |
|-------------------------|-------------------------------------------|
| Eren VURAL              |[erenvural](https://github.com/erenvural)  |
| Mahmut KOÇAKER          |[mkocaker06](https://github.com/mkocaker06)|
| Muhammed Olcay TERCANLI |[molcay](https://github.com/molcay)        |