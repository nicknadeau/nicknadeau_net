import sys
import os
from html_from_native import *


'''
Generates all of the HTML files from the native sources in the sources root and dumps them into the outRoot, preserving sub-directories.
Ignores any sub-directories named 'include', as well as any hidden files. Only generates HTML from .c files.
'''
def generateAllHtmlFromNativeSources(sourceRoot, outRoot):
	for filename in os.listdir(sourceRoot):
		filepath = os.path.join(sourceRoot, filename)
		if (os.path.isfile(filepath) and filename.endswith(".c")):
			filenameNoExt = os.path.splitext(filename)[0]
			outPath = os.path.join(outRoot, "{}.html".format(filenameNoExt))
			generateHtmlFromNativeSource(filepath, filenameNoExt, outPath)
		elif (os.path.isdir(filepath)):
			if (filename != "include"):
				# Recursively call back into ourselves for this new directory.
				newSourceRoot = os.path.join(sourceRoot, filename)
				newOutRoot = os.path.join(outRoot, filename)
				if not os.path.exists(newOutRoot):
					os.mkdir(newOutRoot)
				generateAllHtmlFromNativeSources(newSourceRoot, newOutRoot)


# Generates the index.html file and writes it to the given outRoot. It will automatically redirect to the /about.html file.
def generateRedirectIndexHtml(outRoot):
	index = os.path.join(outRoot, "index.html")
	with open(index, "w") as indexFile:
		indexFile.write('<!DOCTYPE html>\n')
		indexFile.write('<html>\n')
		indexFile.write('\t<head>\n')
		indexFile.write('\t\t<title>Nick Nadeau</title>\n')
		indexFile.write('\t\t<meta name="description" content="Nick Nadeau\'s website.">\n')
		indexFile.write('\t\t<meta name="viewport" content="width=device-width, initial-scale=1">\n')
		indexFile.write('\t\t<meta http-equiv="refresh" content="0; URL=/about.html">\n')
		indexFile.write('\t</head>\n')
		indexFile.write('\t<body>\n')
		indexFile.write('\t</body>\n')
		indexFile.write('</html>\n')


'''
Note: since this function only generates new sources and does not know whether something has been deleted, the best practice is to delete
the html/ output directory in the repository root before running so that the entire contents of it get re-generated again.
'''
if __name__ == '__main__':
	if (len(sys.argv) == 3):
		# Get the absolute path of the repo we are in.
		absProgramPath = os.path.abspath(sys.argv[0])
		repoRoot = os.path.dirname(os.path.dirname(absProgramPath))

		# Create the absolute path of the directory containing the native source files.
		sourceRoot = os.path.abspath(sys.argv[1])

		# Create the absolute path of the directory where the generated HTML output files will go.
		outRoot = os.path.abspath(sys.argv[2])
		if not os.path.exists(outRoot):
			os.mkdir(outRoot)
			generateRedirectIndexHtml(outRoot)

		print("Generating ALL html files from the native source files at {} ...".format(sourceRoot))
		generateAllHtmlFromNativeSources(sourceRoot, outRoot)
		print("Successfully generated ALL html files from native sources: {}".format(outRoot))
	else:
		print("USAGE: python3 {} <source-dir> <out-dir>".format(sys.argv[0]), file=sys.stderr)
		exit(1)
