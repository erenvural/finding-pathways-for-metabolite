#!/usr/bin/python
import sys, json, webbrowser

metabolite_name = sys.argv[1]

HTML_TEMPLATE = """<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
	<meta name="description" content="">
	<meta name="author" content="">
	<link rel="icon" href="../../favicon.ico">

	<title>Search Results for: {0}</title>

	<!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="../assets/bootstrap.min.css"/>

	<!-- Latest compiled and minified JavaScript -->
	<script src="../assets/bootstrap.min.js"></script>

	<!-- Our stylesheet file -->
	<link rel="stylesheet" href="../assets/style.css"/>
</head>
<body>
<div class="container">
	<h1> Search Result for: {0} </h1>
	<div class="results table-responsive col-md-12">
		<table class="table table-striped table-condensed table-hover">
			<thead>
				<tr>
					<th>#</th>
					<th>Matching Type:With (M/S/P)</th>
					<th>Pathway Name</th>
					<th>Pathway URL</th>
				</tr>
			</thead>
			<tbody>
				{1}
			</tbody>
		</table>
	</div>
</div>
<footer class="footer">
	<div class="container">
		<p class="text-muted">&copy; 2017</p>
	</div>
</footer>
</body>
</html>
"""

with open('output/{}.json'.format(metabolite_name), 'r') as fp:
		result = json.load(fp)

inner_html = ""
for pathway_scr in result['pathways'].keys():
	inner_html += """
				<tr>
					<th colspan="4">{0}</th>
				</tr>
				""".format(pathway_scr.title())
	for (i, pathway) in enumerate(result['pathways'][pathway_scr]):
		if 'parent' in pathway['parent'].keys():
			parent_type = pathway['parent']['parent']['type']
			parent_name = pathway['parent']['parent']['name']
			match_type = "P"
		else:
			parent_type = pathway['parent']['type']
			parent_name = pathway['parent']['name']
			match_type = pathway['parent']['type']
		inner_html += """
					<tr>
						<td>{0}</td>
						<td>{3}:{4}</td>
						<td>{1}</td>
						<td><a target="_blank" href="{2}">{2}</a></td>
					</tr>
					""".format(i+1, pathway['name'], pathway['url'], match_type, parent_name)

# print(HTML_TEMPLATE.format(metabolite_name, inner_html))


with open('output/{}.html'.format(metabolite_name), 'w') as fp:
		fp.write(HTML_TEMPLATE.format(metabolite_name, inner_html))

webbrowser.open("output/{}.html".format(metabolite_name))
