import sys
import os


# Creates the htmlOutPath file and auto-generates its html contents from the given native source file contents.
def generateHtmlFromNativeSource(nativeSourcePath, sourceName, htmlOutPath):
	with open(htmlOutPath, "w") as outFile:
		outFile.write('<!DOCTYPE html>\n')
		outFile.write('<html>\n')
		outFile.write('\t<head>\n')
		outFile.write('\t\t<title>Nick Nadeau - {}</title>\n'.format(sourceName))
		outFile.write('\t\t<meta name="description" content="Nick Nadeau\'s {} page.">\n'.format(sourceName))
		outFile.write('\t\t<meta name="viewport" content="width=device-width, initial-scale=1">\n')
		outFile.write('\t</head>\n')
		outFile.write('\t<body>\n')
		isFirstLine = True
		try:
			with open(nativeSourcePath, "r") as sourceFile:
				lines = sourceFile.readlines()
				for line in lines:
					lineSplit = line.splitlines()
					for linePart in lineSplit:
						if isFirstLine:
							outFile.write("\t\t{}\n".format(linePart))
							isFirstLine = False
						else:
							outFile.write("\t\t<br>{}\n".format(linePart))
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
