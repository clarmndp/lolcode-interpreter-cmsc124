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
from lexer import Lexer
import parser
import re
symbol_table = {}
lexeme_table=[]

arithmetic_patterns= ["SUM OF ", "DIV OF", "ADD OF ", "PRODUKT OF", "QUOSHUNT OF"]


# def arithmetic_operation(operand):
#     def evaluate_add():

#     if operand.startswith('SUM OF'):
#         tokenized= re.split("SUM OF ",operand,1)
#         tokenized.pop(0)
        
#         print(tokenized)
#     elif operand.startswith("DIFF OF"):
#         tokenized= re.split("DIFF OF ",operand,1)
#     pass

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
                    line=line.strip() # Rmoves the white spaces around the line
                    tokenize= Lexer.definer(line)
                   
                    parse= parser.Parser(tokenize)
                    parse_tree = parse.parse()
                
                    # if line.startswith("VISIBLE"):
                    #     tokenized= line.split("VISIBLE ")
                    #     tokenized[0]="VISIBLE"
                       
                    #      # Pop the empty element of the list 
                    #     if tokenized[1].startswith("\""): # String literal printing
                    #         tokenized[1]= tokenized[1].strip("\"")
                    #         print(tokenized[1])
                            
                    #     else:
                    #         #valid variable 
                    #         if tokenized[1] in symbol_table.keys():
                    #             print(symbol_table[tokenized[1]])
                               

                    #         else:
                    #             print(f"Variable {tokenized[1]} does not exist in the dictionary")
                    # elif line.startswith("I HAS A"):
                    #     #We want to seperate I HAS A as a whole
                    #     #We can just remove it then re add it
                    #     tokenized= line.split("I HAS A ")
                    #     tokenized.pop(0)  
                    #     tokenized= tokenized[0].split(" ")

                    #     tokenized.insert(0," I HAS A")
                        
                        
                    #     # tokenized= tokenized[].split(" ")
                        
                    #     if  re.match(r"^[A-Z a-z]", tokenized[1]): # Valid variable name
                           
                    #         symbol_table[tokenized[1]]=tokenized[3]
                    #     else:
                    #         print("Variable Error: Not a valid variable name")
                    # elif line.startswith("GIMMEH"):
                    #     tokenized= line.split("GIMMEH ")
                    #     tokenized[0]="GIMMEH"
                    #     if tokenized[1] not in symbol_table.keys():
                    #         print(f"Variable {tokenized[1]} is not known")
                    #         return
                    #     else:
                    #         temp=str(input(""))
                    #         symbol_table[tokenized[1]]=temp 
                    # else:
                    #     print("Unknown Line")
                    #     exit()
                               
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")

def analyzeTokens(tokens):
    """ Process the tokens from each line
        Check token types here 
    """
    print(lexeme_table)
    # for i in lexeme_table:
    #     for token in i:
    #         print(f"Token: {token.type} = {token.value}")

# Start
def main():
    if len(sys.argv) != 2:
        print("Error: Must be of format > python main.py <filename.lol>")
        exit()
    
    program_file = sys.argv[1]
    interpreter(program_file)

if __name__ == "__main__":
    main()
# print(arithmetic_operation("SUM OF SUM OF 3 AN 5 AN 5"))