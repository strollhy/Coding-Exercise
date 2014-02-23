import json

class Loader:
	""" Data loader

	Load data from local file 'data.csv' into memory

    """ 
	def __init__(self, filestream):
		""" Load data into memory """
		# Load head and each entry
		self.head = [h.strip() for h in filestream.next().split(",")]
		self.entry = []
		
		for line in filestream:
			row = [i.strip() for i in line.split(",")]
			self.entry.append(row)

		# Sort by Run Number
		self.entry.sort(key = lambda x:x[2])

	def display(self):
		""" Display data in console """
		print self.head
		for row in self.entry:
			print "%s" % row,

	def output(self):
		""" Return data in JSON """
		return json.dumps(self.entry)

if __name__ == '__main__':
	f = open("test.csv")
	loader = Loader(f)
	#loader.display()
	print loader.output()