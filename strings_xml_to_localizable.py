import sys
import re

def transform_android_string(android_string):
	transformed = re.sub(r'(?:<string name=\"|<string name = \")', '\"', android_string) #convert string tags
	transformed = re.sub(r'\">', '\" = ', transformed)
	transformed = re.sub(r'</string>', ';', transformed)
	transformed = re.sub(r'<!--', '/*', transformed) #convert xml comments
	transformed = re.sub(r'-->', '*/', transformed)
	transformed = re.sub(r'<resources>', '', transformed) #strip resource tags
	transformed = re.sub(r'</resources>', '', transformed)
	#todo: universal conversion of all entities
	transformed = re.sub(r'&#8230;', '\\U2026', transformed) #convert xml entity ellipse to unicode
	return transformed

def convert_android_to_ios(input_file_name, output_file_name):
	inputfile = open(input_file_name,'r')
	outputfile = open(output_file_name, 'w')
	outputfile.write(transform_android_string(inputfile.read()))
	outputfile.close()
	inputfile.close()

def assert_true(condition, message):
	if condition:
		print "OK " + message
	else:
		print "FAIL " + message

def test_convert_string_tag():
	assert_true(transform_android_string("""<string name="test_string">"test string"</string>""") == """"test_string" = "test string";""", "convert string")
	assert_true(transform_android_string("""<string name="test_string">"test \\"string\\""</string>""") == """"test_string" = "test \\"string\\"";""", "convert string with escaped quotes")

def test_convert_ellipse_entity():
	assert_true(transform_android_string("""&#8230;""") == """\\U2026""", "convert ellipse entity")
	assert_true(transform_android_string("""&#8230;&#8230;&#8230;""") == """\\U2026\\U2026\\U2026""", "convert ellipse entity multiple")

def test_strip_resource_tags():
	assert_true(transform_android_string("""<resources>resource tags</resources>""") == """resource tags""", "strip resource tags")

def test_convert_comment():
	assert_true(transform_android_string("""<!-- comment -->""") == """/* comment */""", "convert comment")
	assert_true(transform_android_string("""<!-- comment --> <!-- comment -->""") == """/* comment */ /* comment */""", "convert comment multiple")

def run_all_tests():
	test_convert_string_tag()
	test_convert_comment()
	test_strip_resource_tags()
	test_convert_ellipse_entity()

# Very simple tool to convert an android strings.xml file to an iOS Localizable.strings file
# This does not currently handle complex android strings
def main(argv):
	num_args = len(argv)

	if num_args == 1 and argv[0] == "-test":
	   run_all_tests()
	   sys.exit(0)

	if num_args != 2:
		print 'Converts an Android strings.xml to an iOS Localizable.strings'
		print 'Assumes a well formed strings.xml with quotes around each string value. Run clean_android_strings.py first, to ensure.'
		print 'Usage: <input.xml> <output.strings>'
		print '   or'
		print 'Usage: -test (run all tests)'		
		sys.exit(2)
	convert_android_to_ios(argv[0], argv[1])

if __name__ == "__main__":
	main(sys.argv[1:])