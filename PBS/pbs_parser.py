__author__ = 'jamiebrew'

import os
import string
import operator

"""
Takes a transcript formatted as follows, with newlines separating lines, and without paragraph breaks in the middle of
lines. (this is how transcripts are formatted on genius.com)

Pulls the transcript from 'raw_transcripts/name]' and saves them to 'texts/transcripts/[name]'

[[
CHARACTER: I am saying a line and I am using a VARIety of CapITALIzations and   spacing    patterns

Some more text in character's line here.

OTHER CHARACTER: Okay...

Here are some stage directions in a separate paragraph that does not contain a colon. The characters are kissing
each other.

]]

Feeds these into separate text files, each containing the collection of lines spoken by a particular character,
each named after the character. Also creates a file called "stage directions" that has all of the lines that did
not seem to be attributed to a character.

NOTES:

Assumes that lines are attributed using a colon.

Assumes that colons do not appear in stage direction paragraphs.

Does not know about alternate names for the same character. WILLY LOMAN and WILLY will be fed into different files.
Likewise, WILLY (to himself) will be fed into a different file from WILLY.

"""




class transcript_parser(object):

	def parse(self, path, dname):
		with open(path, "r") as f:
			lines = f.read().replace('\n',' ').split('###LINE###')
			for line in lines:
				if len(line.split(':')) > 1:
					speaker = line.split(':')[0].replace('/','-').strip()[0:60]
					line = '\n'.join(line.split(':')[1:])
					savepath = 'PBS/%s_speakers/%s' % (dname, speaker)
					if os.path.isfile(savepath):
						with open(savepath, 'a') as savefile:
							savefile.write(line)
					else:
						with open(savepath, 'w') as savefile:
							savefile.write(line)


	def biggest_characters(self, tname, number):
		size_by_name = {}
		tpath = 'texts/transcripts/%s' % tname
		for cname in os.listdir(tpath):
			cpath = '%s/%s' % (tpath, cname)
			size_by_name[cname] = len(file(cpath).read().split())
		sorted_chars = list(reversed(sorted(size_by_name.items(), key=operator.itemgetter(1))))
		for pair in sorted_chars[0:number]:
			print pair
		return sorted_chars


p = transcript_parser()
dname = 'PBS/history'

for fname in os.listdir(dname)[0:40]:
	path = '%s/%s' % (dname, fname)
	p.parse(path, dname.split('/')[1])