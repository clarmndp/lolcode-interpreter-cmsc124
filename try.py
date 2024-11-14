file= open("test.lol","r")
starting = file.readline().strip()

variable={} # Dictionary for keeping the variables
if starting != "HAI":
    print("Error Invalid Starting Keyword")
    exit()
for line in file:
    line=line.strip() # Rmoves the white spaces around the line
    if line.startswith("VISIBLE"):
        tokenized= line.split("VISIBLE ")
        tokenized.pop(0) # Pop the empty element of the list 
        tokenized= tokenized[0].strip("\"")
        print(tokenized)

