#!/usr/bin/python
# coding: utf-8

import json
import requests


def main(args):
	response = requests.get("https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=1&titles="+args[0]+"&exintro&exlimit=1&exsentences=1")
	content=json.loads(response.content)
	extract=""
	try:
		pages=content['query']['pages']
		for page in pages.values():
			extract=page['extract']
	except Exception:
		print("not found")
	return extract