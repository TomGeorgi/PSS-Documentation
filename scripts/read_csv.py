def read_data(self, path):
	with open(path, 'r', newline='\r\n') as data:
		reader = csv.DictReader(self.__skip_comments(data), delimiter=';')
		test_data = []
		for row in reader:
			test_data.append(row)
			
		return test_data
            
def __skip_comments(self, lines):
	for index, line in enumerate(lines):
		line = re.sub(re.compile(r'\s*#.*$'), '', line).strip()
		if line:
			yield line