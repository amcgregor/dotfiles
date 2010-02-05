# encoding: utf-8

"""
Parse an input CSV file, cleaning cells as you.

Transcribes from 'input.csv' into 'output.csv' while simultaneously
breaking the input into files containing no more than 20 records each.

Breaking apart helps one narrow down which record is causing trouble.

Additionally replaces unicode "extended characters" (like the curly
quotes misused by Microsoft Office software) into the nearest ASCII
equivalant, and replaces newlines in the input with a space.

Written to un-fsck 1200 records of Outlook contact information for
input into Apple Address Book.  The process was this:

    1. Export to Excel from Outlook.
    2. Upload Excel document to Google Docs.
    3. Export from Google Docs to CSV.
    4. Run through this script.
    5. Import & wait.

Enjoy!

    - Alice.

This code is public domain.
"""

from __future__ import with_statement

import csv
import codecs

import vobject


i = 0
first = None


with open("input.csv", 'r') as rf:
	reader = csv.reader(rf, delimiter=',', quotechar='"')
	
	with open("fixed.csv", 'w') as wf:
		writer = csv.writer(wf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		part = open("chops/%i.csv" % (i // 20, ), 'w')
		partwriter = csv.writer(part, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		
		for row in reader:
			if i == 0:
				first = row
				i += 1
				writer.writerow(first)
				partwriter.writerow(first)
				continue
			
			if i % 20 == 0:
				part.close()
				part = open("chops/%i.csv" % (i // 20, ), 'w')
				partwriter = csv.writer(part, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				partwriter.writerow(first)
			
			columns = []
			
			empty = True
			
			for col in row:
				if col.strip():
					empty = False
				
				try:
					col.decode('ascii')
				
				except UnicodeDecodeError:
					print 'Row', i, 'contains unicode characters; fixing.'
				
				columns.append(codecs.encode(col.decode('utf8').replace('\n', ' ').replace('\t', ' '), 'ascii', 'replace'))
			
			if empty:
				print 'Row', i, 'is empty, not transcribing.'
				i += 1
				continue
			
			writer.writerow(columns)	
			partwriter.writerow(columns)	
			
			i += 1