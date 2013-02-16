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
	# handle edge case of [string \"quote at end\"] --> ["string \"quote at end\""]
	transformed = re.sub(r'\\\"</string>', '\\\"\"</string>', transformed)
	transformed = re.sub(r'\"?</string>', '\"</string>', transformed) 
	transformed = re.sub(r'">"?', '">"', transformed)
	return transformed

def clean_android_strings(input_file_name, output_file_name):
	inputfile = open(input_file_name,'r')
	outputfile = open(output_file_name, 'w')
	outputfile.write(clean_android_string(inputfile.read()))
	outputfile.close()
	inputfile.close()

def assert_true(condition, message):
	if condition:
		print "OK " + message
	else:
		print "FAIL " + message

def test_trim_newline_whitespace():
	assert_true(clean_android_string("""<string name="test_newline">"   \\n   "</string>""") == """<string name="test_newline">"\\n"</string>""", "newline before after")
	assert_true(clean_android_string("""<string name="test_newline">"\\n   "</string>""") == """<string name="test_newline">"\\n"</string>""", "newline after")
	assert_true(clean_android_string("""<string name="test_newline">"   \\n"</string>""") == """<string name="test_newline">"\\n"</string>""", "newline before")
	assert_true(clean_android_string("""<string name="test_newline">"   \\n   \\n  \\n  "</string>""") == """<string name="test_newline">"\\n\\n\\n"</string>""", "newline multiple")

def test_add_quotes():	
	assert_true(clean_android_string("""<string name="test_add_quotes">add quotes around this</string>""") == """<string name="test_add_quotes">"add quotes around this"</string>""", "add quotes")
	assert_true(clean_android_string("""<string name="test_add_quotes">add quotes around \\"this\\"</string>""") == """<string name="test_add_quotes">"add quotes around \\"this\\""</string>""", "add quotes escaped quote at end")

def test_ellipse_conversion():
	assert_true(clean_android_string("""<string name="test_ellipse">"..."</string>""") == """<string name="test_ellipse">"&#8230;"</string>""", "ellipse conversion")
	assert_true(clean_android_string("""<string name="test_ellipse">"   ..."</string>""") == """<string name="test_ellipse">"&#8230;"</string>""", "ellipse prior space")
	# note: is this next test a bug or a feature, removing all preceeding whitespace with multiple ellipses? :)
	assert_true(clean_android_string("""<string name="test_ellipse">"... ... ......"</string>""") == """<string name="test_ellipse">"&#8230;&#8230;&#8230;&#8230;"</string>""", "ellipse multiple")

def test_escape_quotes():
	assert_true(clean_android_string("""<string name="test_quotes">"\\\\"slash quote\\\\""</string>""") == """<string name="test_quotes">"\\"slash quote\\""</string>""", "escaped quotes")
	assert_true(clean_android_string("""<string name="test_quotes">"\\"slash quote\\""</string>""") == """<string name="test_quotes">"\\"slash quote\\""</string>""", "escaped quotes no action")
	assert_true(clean_android_string("""<string name="test_quotes">"\\"slash quote\\" \\\\""</string>""") == """<string name="test_quotes">"\\"slash quote\\" \\""</string>""", "escaped quotes multiple")

def run_all_tests():
	test_trim_newline_whitespace()
	test_ellipse_conversion()
	test_add_quotes()
	test_escape_quotes()

# Very simple tool to cleanup an android strings.xml file
def main(argv):
	num_args = len(argv)

	if num_args == 1 and argv[0] == "-test":
	   run_all_tests()
	   sys.exit(0)

	if num_args != 2:
		print 'Cleans an Android strings.xml'
		print 'Usage: <input.xml> <output.xml>'
		print '   or'
		print 'Usage: -test (run all tests)'
		sys.exit(2)


	clean_android_strings(argv[0], argv[1])

if __name__ == "__main__":
	main(sys.argv[1:])