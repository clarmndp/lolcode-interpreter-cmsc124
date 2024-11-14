import re
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
        if tokenized[0].startswith("\""): # String literal printing
            tokenized= tokenized[0].strip("\"")
            print(tokenized)
            
        else:
            
            if re.match(r"^[A-Z a-z]", tokenized[0]): #valid variable
                if tokenized[0] in variable.keys():
                    print(variable[tokenized[0]])
                else:
                    print(f"Variable {tokenized[0]} does not exist in the dictionary")
    elif line.startswith("I HAS A"):
        tokenized=line.split("I HAS A ")
        tokenized.pop(0)
        tokenized= tokenized[0].split(" ")
        variable[tokenized[0]]=tokenized[2].strip("\"")
        print(tokenized)
                

