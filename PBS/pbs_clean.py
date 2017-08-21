import os

d = 'PBS/nature/'
for filename in os.listdir(d)[1:]:
	path = d + filename
	print path
	with open(path, 'r') as f:
		text = f.read()
		words = text.split()


		#print "words",len(words)
		if len(text.split('This is PBS')) == 2:
			pruned = text.split('This is PBS')[0]
			print 'This is PBS'
		elif len(text.split('Presented by')) ==2:
			pruned = text.split('Presented by')[0]
			print 'Presented by'
		elif len(text.split('Written by')) ==2:
			pruned = text.split('Written by')[0]
			print 'Written by'
		elif len(text.split('Edited by')) ==2:
			pruned = text.split('Edited by')[0]
			print 'Edited by'
		elif len(text.split('On NOVA')) ==2:
			pruned = text.split('On NOVA')[0]
			print 'On NOVA'
		elif len(text.split('To order this show')) ==2:
			pruned = text.split('To order this show')[0]
			print 'To order this show'
		elif len(text.split('NOVA is a production')) ==2:
			pruned = text.split('NOVA is a production')[0]
			print 'NOVA is a production'
		else:
			print "NONE NONE NONE NONE NONE NONE NONE NONE NONE NONE"
			pruned = text



		savepath = 'PBS/nature_clean/%s' % filename
		with open(savepath, 'w') as wf:
			wf.write(pruned)
			#print pruned[-500:]
