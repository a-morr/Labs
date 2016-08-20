import numpy as np
import string
import scipy.sparse as sp
import sys
import pickle

def create_data(filename):

	'''
	This creates the data from the raw stack exchange file at
	https://archive.org/download/stackexchange

	Just click on the math one to download it
	'''
	
	# Read data in
	with open(filename, 'r') as f:
		contents = f.read().split('\n')
	if contents[-1] == "":
		contents = contents[:-1]

	# Create file for writing
	outfile = 'stack_exchange_posts'
	ofile = open(outfile, 'w')

	# This data is seriously jacked and so we are going to exclude a ton of stuff.  We
	# could exclude a lot more but I am getting really sick and tired of it and its good enough.
	# The following is a list of prohibited first line characters.
	prohibited = ['$', '$$', '=', '\\', '+', '{', '{', '0', '-']
	tot = len(contents)
	count = 0
	error_count = 0
	for line in contents:
		sys.stdout.write('Working line ' + str(count) + ' of ' + str(tot) + '\r')
		sys.stdout.flush()

		# Only keep the lines we want.
		if len(line) > 0 and line[0] not in prohibited and not line.count('$') % 2 and not line.count('$$') % 2:
			try:
				# This is a whole bunch of hocus pocus to get rid of the math symbols and keep the english.
				# Could probably be replaced with a clever regular expression.
				line = line.split('$$')
				if int(len(line)/2.):
					new_line = ''
					for i in xrange(int(len(line)/2.) + 1):
						new_line= new_line + line[2*i]
				else:
					new_line = line[0]

				new_line = new_line.split('$')
				if int(len(new_line)/2.):
					line = ''
					for i in xrange(int(len(new_line)/2.) + 1):
						line = line + new_line[2*i]
				else:
					line = new_line[0]
				
				# Strip punctation
				line = line.translate(string.maketrans("",""), string.punctuation)
				line = line.split(' ')
				#print line
				flag = 0
				for word in line:
					if not any(char.isdigit() for char in word) and len(word) < 12 and ' ' not in word:
						ofile.write(word + ' ')
						flag = 1
				if flag:
					ofile.write('\n')
			except IndexError:
				# This should only happen a few times.  Don't worry too much.
				#print "ERROR!"
		# If you want a diagnostic tool, you can use this.
				error_count += 1
		
		count = count + 1
	ofile.close()
	print str(error_count) + " Errors.  Don't sweat it."
	
def create_word_list(filename):
	'''
	Create a word list from the data file we created.
	'''
	file = open(filename, 'r')
	file = file.read()
	file = file.split('\n')
	file = file[:-1]

	outfile = filename + '_numbers'
	outfile = open(outfile, 'w')

	word_list = []
	index = 0
	count = 0
	for line in file:
		sys.stdout.write('Working line ' + str(count) + ' of ' + str(len(file)) + '\r')
		sys.stdout.flush()
		line = line.upper()
		line = line.split(' ')
		for word in line:
			if word not in word_list:
					word_list.append(word)
					outfile.write(str(index) + ' ')
					index = index + 1
			else:
				outfile.write(str(word_list.index(word)) + ' ')
		outfile.write('\n')
		count += 1
	
	outfile.close()
	return word_list

def generate_chain(filename, dim):
	
	'''
	Generates the transition matrix.
	More complicated than it needs to be.
	'''

	file = open(filename, 'r')
	file = file.read()
	file = file.split('\n')
	file = file[:-1]

	dim += 2
	outdegree = np.zeros(dim, dtype='float')
	chain = sp.lil_matrix((dim, dim))

	tot = len(file)
	count = 0
	for line in file:
		sys.stdout.write('Working line ' + str(count) + ' of ' + str(tot) + '\r')
		sys.stdout.flush()
		if line != '':
			words = line.split(' ')
			#Increment start state to first word
			chain[0, int(words[0])]  += 1
			outdegree[0] += 1
		
			current_word = int(words[0])
			for word in words[1:-1]:
				chain[int(word) + 1, current_word + 1] += 1
				outdegree[current_word + 1] += 1
				current_word = int(word)
			#Increment last word to stop state.
			chain[dim - 1, current_word] += 1
			outdegree[current_word + 1] += 1
		count += 1
	'''
	for i in xrange(len(outdegree)):
		chain[:,i] = chain[:,i] / float(outdegree[i])
	'''
	
	chain = chain.T
	print "Multiplying"
	for i in xrange(len(outdegree)):
		sys.stdout.write(str(i) + ' of ' + str(len(outdegree)) + '\r')
		sys.stdout.flush()
		if outdegree[i] != 0:
			chain[i,:] *= 1./outdegree[i]
	chain = chain.T
	
	return chain, outdegree

def simulate_chain(chain):
	
	current_word = 0
	
	chain = chain.T # This improves performance.
	sentence = []
	while current_word != chain.shape[0] - 1:
		if current_word != chain.shape[0] - 1:
			vec = np.random.multinomial(1, chain[current_word,:].toarray()[0])
			current_word = np.where(vec)[0][0]
			sentence.append(current_word)
	return sentence

def print_sentence(sentence, word_list):
	
	s1 = word_list[sentence[0] - 1]
	for word in sentence[1:-1]:
		s1 = s1 + ' ' + word_list[word - 1]
	s1 = s1[:-1] + '.'
	
	print s1

def some_sentences(chain, word_list, n=10):

	for i in xrange(n):
		s = simulate_chain(chain)
		print "Sentence " + str(i+1) + ":"
		print_sentence(s, word_list)
		print '' 

filename = 'math.stackexchange.com.7z'
print "Creating Data"
create_data(filename)
print "\nCreating Word List"
word_list = create_word_list('stack_exchange_posts')
pickle.dump(word_list, open('word_list.p', 'wb'))
print "Creating Chain"
chain, outdegree = generate_chain('stack_exchange_posts_numbers', len(word_list))
some_sentences(chain, word_list)
