import sys
import re

def transform_android_string(android_string):
	transformed = re.sub(r'(?:<string name=\"|<string name = \")', '\"', android_string) #convert string tags
	transformed = re.sub(r'\">\"?', '\" = \"', transformed)
	transformed = re.sub(r'\"?</string>', '\";', transformed)
	transformed = re.sub(r'<!--', '/*', transformed) #convert xml comments
	transformed = re.sub(r'-->', '*/', transformed)
	transformed = re.sub(r'<resources>', '', transformed) #strip resource tags
	transformed = re.sub(r'</resources>', '', transformed)
	transformed = re.sub(r'&#8230;', '\\U2026', transformed) #convert xml entity ellipse to unicode
	return transformed

def convert_android_to_ios(input_file_name, output_file_name):
	inputfile = open(input_file_name,'r')
	outputfile = open(output_file_name, 'w')
	outputfile.write(transform_android_string(inputfile.read()))
	outputfile.close()
	inputfile.close()

# Very simple tool to convert an android strings.xml file to an iOS Localizable.strings file
# This does not currently handle complex android strings
def main(argv):
	num_args = len(sys.argv)
	if num_args != 3:
		print 'Converts an Android strings.xml to an iOS Localizable.strings'
		print 'Usage: <input.xml> <output.strings>'
		sys.exit(2)
	convert_android_to_ios(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
	main(sys.argv[1:])