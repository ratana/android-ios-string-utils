import sys
import re

def clean_android_string(android_string):
	#\\" -> \" 
	transformed = re.sub(r'\\\\"', '\\"', android_string) 
	#... -> ellipse, remove whitespaces before ellipse
	transformed = re.sub(r'\s*\.\.\.', '&#8230;', transformed) 
	#trim whitespace around \n
	transformed = re.sub(r'\s*\\n\s*', re.escape('\\') + 'n', transformed)
	#place quotes around strings inside xml tags that do not have them
	transformed = re.sub(r'\"?</string>', '\"</string>', transformed) 
	transformed = re.sub(r'">"?', '">"', transformed)
	return transformed

def clean_android_strings(input_file_name, output_file_name):
	inputfile = open(input_file_name,'r')
	outputfile = open(output_file_name, 'w')
	outputfile.write(clean_android_string(inputfile.read()))
	outputfile.close()
	inputfile.close()

# Very simple tool to cleanup an android strings.xml file
def main(argv):
	num_args = len(sys.argv)
	if num_args != 3:
		print 'Cleans an Android strings.xml'
		print 'Usage: <input.xml> <output.xml>'
		sys.exit(2)
	clean_android_strings(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
	main(sys.argv[1:])