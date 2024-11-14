"""
# LOLCODE Interpreter written in Python
    
    Authors:
        Diño, John Matthew D.
        Mandap, Clarence P.
        Pore, Richmond Michael B.

    Components/ modules:
        lexer.py - Handles tokenization and lexical analysis
        main.py - Ties all components together and handles program execution
"""

import sys
from lexer import Token, Lexer, TOKEN_TYPES

def interpreter(filename):
    # We first check if the file extension is .lol
    if not filename.endswith('.lol'):
        print("Error: File must have '.lol' extension")
        exit()
        
    try:
        with open(filename, 'r') as file:
            # Read the first line and check for HAI
            starting = file.readline().strip()
            if starting != "HAI":
                print ("Error: Invalid Starting Keyword")
                exit()

            # Proceed to the rest of the LOLCODE file
            for line in file:
                line = line.strip() # Removes the white spaces around the line
                if line:  # Skip empty lines
                    tokens = Lexer.tokenizer(line)
                    analyzeTokens(tokens)               
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")

def analyzeTokens(tokens):
    """ Process the tokens from each line
        Check token types here 
    """
    for token in tokens:
        print(f"Token: {token.type} = {token.value}")

# Start
def main():
    if len(sys.argv) != 2:
        print("Error: Must be of format > python main.py <filename>")
        exit()
    
    program_file = sys.argv[1]
    interpreter(program_file)

if __name__ == "__main__":
    main()