import sys
import os


TAB_PIXEL_SIZE = 25


# Returns the number of leading tab characters in the line. (eg. \t\to\t would return 2 not 3).
def getNumLeadingTabs(line):
	tabCount = 0
	for character in line:
		if (character == '\t'):
			tabCount += 1
		else:
			break;
	return tabCount


'''
Returns the same line of native code except with HTML+CSS formatting so that it renders correctly on the web.
Note: this will not provide a font style and it will not add any left margins for tabs. This only focuses on displaying the line contents
in this isolated context correctly.
'''
def formatNativeCodeLine(line):
	#TODO: actually style the line contents.
	return line


# Creates the htmlOutPath file and auto-generates its html contents from the given native source file contents.
def generateHtmlFromNativeSource(nativeSourcePath, sourceName, htmlOutPath):
	with open(htmlOutPath, "w") as outFile:
		outFile.write('<!DOCTYPE html>\n')
		outFile.write('<html>\n')
		outFile.write('\t<head>\n')
		outFile.write('\t\t<title>Nick Nadeau - {}</title>\n'.format(sourceName))
		outFile.write('\t\t<meta name="description" content="Nick Nadeau\'s {} page.">\n'.format(sourceName))
		outFile.write('\t\t<meta name="viewport" content="width=device-width, initial-scale=1">\n')
		outFile.write('\t\t<link href="https://fonts.googleapis.com/css?family=Cutive Mono" rel="stylesheet">\n')
		outFile.write('\t\t<link href="/styles/style-main.css" rel="stylesheet">\n')
		outFile.write('\t</head>\n')
		outFile.write('\t<body>\n')
		isFirstLine = True
		try:
			with open(nativeSourcePath, "r") as sourceFile:
				lines = sourceFile.readlines()
				for line in lines:
					# Split the line on newline delimiters.
					lineSplit = line.splitlines()
					for linePart in lineSplit:
						# Count the number of leading tabs in this part of the line. This determines how much left padding to add to give the appearance of tabs.
						tabCount = getNumLeadingTabs(linePart)
						leftPad = tabCount * TAB_PIXEL_SIZE
						# Re-format the line for HTML so that it looks proper.
						formattedLinePart = formatNativeCodeLine(linePart)
						if isFirstLine:
							outFile.write('\t\t<span class="cutive-mono-16" style="margin-left: {}px">{}</span>\n'.format(leftPad, formattedLinePart))
							isFirstLine = False
						else:
							outFile.write('\t\t<br><span class="cutive-mono-16" style="margin-left: {}px">{}</span>\n'.format(leftPad, formattedLinePart))
		except FileNotFoundError as error:
			print("Error: native source file does not exist: {}".format(nativeSourcePath))
			os.remove(htmlOutPath)
			exit(1)
		outFile.write('\t</body>\n')
		outFile.write('</html>\n')


if __name__ == '__main__':
	if (len(sys.argv) == 2):
		# Get the absolute path of the repo we are in.
		absProgramPath = os.path.abspath(sys.argv[0])
		repoRoot = os.path.dirname(os.path.dirname(absProgramPath))

		# Get the name of the source file (extension stripped) and verify it is a .c file.
		absSourcePath = os.path.abspath(sys.argv[1]);
		sourceFilename = os.path.basename(absSourcePath);
		sourceExtSplit = os.path.splitext(sourceFilename)
		sourceExtension = sourceExtSplit[1]
		if (sourceExtension != '.c'):
			print("Error: native source file must be a .c file but found extension: {}".format(sourceExtension), file=sys.stderr)
			exit(1)
		sourceName = sourceExtSplit[0]

		# Create the html output file we will generate.
		outPath = os.path.join(repoRoot, "html", "{}.html".format(sourceName))
		print("Generating html from given native source file...".format(outPath))
		generateHtmlFromNativeSource(absSourcePath, sourceName, outPath)
		print("Successfully generated html from native source: {}".format(outPath))
	else:
		print("USAGE: python3 {} <native-src-file>".format(sys.argv[0]), file=sys.stderr)
		exit(1)
