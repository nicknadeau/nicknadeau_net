import sys
import os


TAB_PIXEL_SIZE = 25
KEYWORDS = """auto const double float int short struct unsigned break continue else for long signed switch void case default enum goto register
	sizeof typedef volatile char do extern if return static union while bool int8_t uint8_t int16_t uint16_t int32_t uint32_t int64_t uint64_t
	""".split()


'''
A simple object which tracks the formatting state. This is long-lived state.
'''
class FormatState:
	def __init__(self):
		self.isEscaped = False
		self.isInString = False
		self.isEscapeEnd = False


'''
The result of updating the format state. This is transient, we hand out one result per update and it is not long-lived.
'''
class UpdateFormatStateResult:
	def __init__(self):
		self.isStringStart = False
		self.isStringEnd = False
		self.isEscapeStart = False
		self.isEscapeEnd = False


'''
Returns the number of leading tab characters in the line. (eg. \t\to\t would return 2 not 3).
'''
def getNumLeadingTabs(line):
	tabCount = 0
	for character in line:
		if (character == '\t'):
			tabCount += 1
		else:
			break;
	return tabCount


'''
Returns true if the given token is a compiler directive.
'''
def isCompilerDirective(state, token):
	return (not state.isEscaped) and (not state.isInString) and token.startswith("#")


'''
Returns true if the given token is a C keyword.
'''
def isKeyword(state, token):
	return (not state.isInString) and (token in KEYWORDS)


'''
Returns true if the given token is a special LINK macro.
'''
def isLinkMacro(state, token):
	return (not state.isEscaped) and (not state.isInString) and token.startswith("LINK(") and token.endswith(")")


'''
Returns true if the given token is an explicit URL.
'''
def isUrl(state, token):
	return "https://" in token


'''
Returns the URL that the link macro should open when clicked.
'''
def getLinkMacroURL(token):
	return "/" + token[5:-1] + ".html"


'''
Returns the explicit URL embedded in the given token.
'''
def getUrl(token):
	startIndex = token.find("https://")
	url = token[startIndex:]
	if url.endswith('"'):
		return url[:-1]
	else:
		return url


'''
Updates the format state given the next character. Invoked BEFORE formatting the character. Used to inform how to format it.
'''
def updateFormatStateBefore(state, character):
	updateResult = UpdateFormatStateResult()
	escape = False
	if not state.isEscaped:
		if character == '\\':
			escape = True
			updateResult.isEscapeStart = True
		elif character == '"':
			state.isInString = (not state.isInString)
			updateResult.isStringStart = state.isInString
			updateResult.isStringEnd = not state.isInString
	updateResult.isEscapeEnd = state.isEscapeEnd
	state.isEscaped = escape
	return updateResult


'''
Updates the format state given the next character. Invoked AFTER formatting the character. Used to inform how to format remaining characters.
'''
def updateFormatStateAfter(state, beforeUpdateResult, character):
	if state.isEscapeEnd:
		# We just processed the escape end, so the escape sequence is over now.
		state.isEscapeEnd = False
	if beforeUpdateResult.isEscapeStart:
		# We just processed the escape start. An escape sequence is 2 characters, so we are now at the escape end next.
		state.isEscapeEnd = True


'''
Returns the same token of native code except with HTML+CSS formatting so that it renders correctly on the web.
'''
def formatNativeCodeToken(state, token):
	formattedToken = ""
	for character in token:
		result = updateFormatStateBefore(state, character)
		if result.isStringStart:
			formattedToken += '<span class="c-string">{}'.format(character)
		elif result.isStringEnd:
			formattedToken += '{}</span>'.format(character)
		elif result.isEscapeStart:
			formattedToken += '<span class="escape-sequence">{}'.format(character)
		elif result.isEscapeEnd:
			formattedToken += '{}</span>'.format(character)
		else:
			formattedToken += character
		updateFormatStateAfter(state, result, character)
	return formattedToken


'''
Injects a hyperlink into the given token. The hyperlink is to the given url and the token is such that it contains this url directly inside it.
Essentially, we want to find the url substring inside token and wrap it inside an 'a href' HTML tag and point it at that url.
'''
def injectHyperlinkInToken(token, url, endWithWhitespace):
	startIndex = token.find(url)
	endIndex = startIndex + len(url)
	front = token[:startIndex]
	back = token[endIndex:]
	return '{}<a href="{}">{}</a>{}{}'.format(front, url, url, back, ' ' if endWithWhitespace else '')


'''
Returns the same line of native code except with HTML+CSS formatting so that it renders correctly on the web.
Note: this will not provide a font style and it will not add any left margins for tabs. This only focuses on displaying the line contents
in this isolated context correctly.
'''
def formatNativeCodeLine(state, line):
	formattedLine = ""
	tokens = line.split()
	for i in range(0, len(tokens)):
		token = tokens[i]
		formattedToken = formatNativeCodeToken(state, token);
		if (isCompilerDirective(state, token)):
			formattedLine += '<span class="compiler-directive">{}</span>{}'.format(formattedToken, ' ' if (i < len(tokens) - 1) else '')
		elif (isKeyword(state, token)):
			formattedLine += '<span class="c-keyword">{}</span>{}'.format(formattedToken, ' ' if (i < len(tokens) - 1) else '')
		elif (isLinkMacro(state, token)):
			url = getLinkMacroURL(token)
			formattedLine += '<a href="{}">{}</a>{}'.format(url, formattedToken, ' ' if (i < len(tokens) - 1) else '')
		elif (isUrl(state, token)):
			url = getUrl(token)
			formattedLine += injectHyperlinkInToken(formattedToken, url, i < len(tokens) - 1)
		else:
			formattedLine += '{}{}'.format(formattedToken, ' ' if (i < len(tokens) - 1) else '')
	return formattedLine


'''
Creates the htmlOutPath file and auto-generates its html contents from the given native source file contents.
'''
def generateHtml(nativeSourcePath, sourceName, htmlOutPath):
	state = FormatState()
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
						formattedLinePart = formatNativeCodeLine(state, linePart)
						if isFirstLine:
							outFile.write('\t\t<span class="cutive-mono-16" style="margin-left: {}px">{}</span>\n'.format(leftPad, formattedLinePart))
							isFirstLine = False
						else:
							outFile.write('\t\t<br><span class="cutive-mono-16" style="margin-left: {}px">{}</span>\n'.format(leftPad, formattedLinePart))
		except FileNotFoundError as error:
			print("Error: native source file does not exist: {}".format(nativeSourcePath))
			os.remove(htmlOutPath)
			return 1
		outFile.write('\t</body>\n')
		outFile.write('</html>\n')
		return 0


'''
Generates an html file from the given native source file and writes it to outDir with the same name as the source file but with extension .html.
Returns 0 on success and 1 on failure. Prints its own error messages.
'''
def generateHtmlFromNativeSource(nativeSourceFile, outDir):
	if not os.path.exists(nativeSourceFile):
		print("Error: native source input file does not exist: {}".format(nativeSourceFile))
		return 1
	if not os.path.isdir(outDir):
		print("Error: HTML out directory does not exist: {}".format(outDir))
		return 1

	# Get the absolute path of the source file, ensure it is a .c file and then strip its extension off.
	absSourcePath = os.path.abspath(nativeSourceFile);
	sourceFilename = os.path.basename(absSourcePath);
	sourceExtSplit = os.path.splitext(sourceFilename)
	sourceExtension = sourceExtSplit[1]
	if (sourceExtension != '.c'):
		print("Error: native source file must be a .c file but found extension: {}".format(sourceExtension), file=sys.stderr)
		return 1
	sourceName = sourceExtSplit[0]

	# Create the html file using the same name as the source file but with the .html extension instead. Then generate the html.
	outFile = os.path.join(outDir, "{}.html".format(sourceName))
	print("Generating {} from native source file {}".format(outFile, absSourcePath))
	return generateHtml(absSourcePath, sourceName, outFile)


if __name__ == '__main__':
	if (len(sys.argv) == 3):
		ret = generateHtmlFromNativeSource(sys.argv[1], sys.argv[2])
		if (ret == 0):
			print("Successfully generated html file!")
		else:
			exit(ret)
	else:
		print("USAGE: python3 {} <native-src-file> <html-out-dir>".format(sys.argv[0]), file=sys.stderr)
		exit(1)
