#To collect the frequency of letters
def frequency(file):
    frequencies = {} #List of letters
    textfile = file + ".txt" #Converts the filename to .txt
	#Opens the text file
    with open(textfile) as freq:
        for line in freq:	#Reads a line
            for char in line: 	#Reads the character 1 by 1
                if char in frequencies:
                    frequencies[char] += 1 #Adds one to the frequency of that letter
                else:
                    frequencies[char] = 1 #If its not in the list then it will add it
    #Sorting the frequency
    frequencies = dict(sorted(frequencies.items(), key = lambda x: x[1]))
    freqkey = frequencies.keys() #Keys the letters from the frequencies
    sortedlist = [] #New list
    for i in freqkey:
        sortedlist.append((frequencies[i],i)) #This reverses the number and the letter for later
    sortedlist.sort() #Sorts list
    return sortedlist #Returns sorted list
    
#Building the tree for the huffman encoding
def treeConstruct(freq):
    while len(freq) > 1:
        lastTwo = tuple(freq[0:2]) #Looks at last two frequencies
        freqList = freq[2:] #This will be the end of the list
        combined = lastTwo[0][0] + lastTwo[1][0] #Adds the numbers of the nodes
        freq = freqList + [(combined,lastTwo)] #Then adds it to the list 
        freq = sorted(freq, key=lambda x: x[0]) #Sorts it every time it goes through
    return freq[0] #Returns the list

def trimTheTree(tree):
	t = tree[1] #It will get rid of the start as it won't be needed as its just whole frequency
	if type(t) is str: #Checks if it is a string instead of a int to get rid of ints
		return t
	else:
		left = trimTheTree(t[0]) #Gets left side
		right = trimTheTree(t[1]) #Gets right side
		trim = (trimTheTree(t[0]),trimTheTree(t[1])) #Combines both sides
		return trim #Returns the trim

def code(node, val='') :
    global codes #Need codes list global to pass to other functions
    if type(node) is str:
        codes[node] = val #Sets value for the letter        
    else:                              
        code(node[0], val+"0") #Left side of branch
        code(node[1], val+"1") #Right side of branch

def encoding(file):
	global codes #Will need the codes to encode the string
	textfile = file + ".txt" #Text file selected
	finaloutput = "" #The final output
	with open(textfile) as string: #Opens the file
		for line in string:
			for char in line:
				finaloutput = finaloutput + codes[char] #Looks at the character and applies the code
	return finaloutput

def saveFileEncoded(output):
	save = input("Name the file you want the output as: ")
	file = save + ".bin"
	decodefile = open(file, 'w') #Opens the file
	decodefile.write(output) #Writes to the output
	decodefile.close() #Closes

def decoding(file, tree):
	binfile = file + ".bin"
	finaloutput = ""
	string = ""
	decode = tree
	
	#Reading the bin file
	with open(binfile, "rb") as f:
		byte = f.read()
	f.close()
	string = byte.decode('utf8')

	#Does the decoding
	for char in string:
		if char == "0":
			decode = decode[0] #Looks left up the tree
		else:
			decode = decode[1] #Looks right up the tree
		if type(decode) is str:
			finaloutput = finaloutput + decode #converting to str
			decode = tree #Restart tree
	return finaloutput


def saveFileDecoded(output):
	save = input("Name the file you want the output as: ")
	file = save + ".txt"
	decodefile = open(file, "w") 
	decodefile.write(output)
	decodefile.close()

def main():
	#Asking for textfile input
	file = input("What is the name of the text file you want to compress: ")

	#Frequencies
	freq = frequency(file) #Gets frequencies
	
	#Tree
	tree = treeConstruct(freq) #Constructs the tree
	finaltree = trimTheTree(tree) #Trims the tree
	
	#Codes
	huffcodes = code(finaltree) #Gets all the codes
	
	#Encoding
	encoded = encoding(file) #Encodes text file
	saveencode = saveFileEncoded(encoded) #Saves the file as a bin file

	#Asking for binfile input
	binfile = input("What is the name of the binfile you saved the compressed file as: ")

	#Decoding
	decoded = decoding(binfile, finaltree)
	savedecode = saveFileDecoded(decoded)

codes = {} #Global variable for the codes
main() #To start the program