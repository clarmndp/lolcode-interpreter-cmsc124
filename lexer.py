# We define token types for lexical analysis
TOKEN_TYPES = {
    "KEYWORD": "KEYWORD",
    "STRING": "STRING",
    "NUMBER": "NUMBER",
    "LITERAL": "LITERAL",
    "IDENTIFIER": "IDENTIFIER",
    "OPERATOR": "OPERATOR",
    "DELIMITER": "DELIMITER",
    "COMMENT": "COMMENT",
    "WHITESPACE": "WHITESPACE",
    "TROOF": "TROOF",
    "NUMBR": "NUMBR",
    "NUMBAR": "NUMBAR"
}

# LOLCODE keywords
KEYWORDS = {
    # Program structure
    "HAI": "program_start",
    "KTHXBYE": "program_end",
    "WAZZUP": "variable_section_start",
    "BUHBYE": "variable_section_end",
        
    # Comments
    "BTW": "single_line_comment",
    "OBTW": "multi_line_comment_start",
    "TLDR": "multi_line_comment_end",
        
    # Variables and assignments
    "I HAS A": "variable_declaration",
    "ITZ": "assignment",
    "R": "assignment_operator",
        
    # Input/output
    "VISIBLE": "print",
    "GIMMEH": "input",

    # Boolean operators
    "BOTH OF": "and",
    "EITHER OF": "or",
    "WON OF": "xor",
    "NOT": "not",
    "ANY OF": "infinite_or",
    "ALL OF": "infinite_and",

    # Arithmetic operators
    "SUM OF": "addition",
    "DIFF OF": "subtraction",
    "PRODUKT OF": "multiplication",
    "QUOSHUNT OF": "division",
    "MOD OF": "modulus",
    "BIGGR OF": "maximum",
    "SMALLR OF": "minimum",
        
    # Comparison operators
    "BOTH SAEM": "equality",
    "DIFFRINT": "inequality",
        
    # String operation
    "SMOOSH": "string_concatenation",
        
    # Type casting
    "MAEK": "cast_operator",
    "A": "cast_delimiter",
    "IS NOW A": "typecast",
        
    # Condition statements
    "O RLY?": "if_start",
    "YA RLY": "then",
    "MEBBE": "else_if",
    "NO WAI": "else",
    "OIC": "if_end",
        
    # Switch cases
    "WTF?": "switch",
    "OMG": "case",
    "OMGWTF": "default_case",
        
    # Loops
    "IM IN YR": "loop_start",
    "UPPIN": "increment",
    "NERFIN": "decrement",
    "YR": "loop_variable",
    "TIL": "until",
    "WILE": "while",
    "IM OUTTA YR": "loop_end",
        
    # Function declarations
    "HOW IZ I": "function_declaration",
    "IF U SAY SO": "function_end",
    "GTFO": "return",
    "FOUND YR": "return_value",
    "I IZ": "function_call",
        
    # Infinite arity
    "MKAY": "infinite_arity_end"
}

class Token:
    """ Parameter 'type' provides the category for TOKEN_TYPES
        Parameter 'value' holds the text/ content
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:  
    # We convert source code by line into tokens
    def tokenizer(line):
        tokens = []
        i = 0
        
        # Boolean keywords
        BOOLEAN_VALUES = {
            "WIN": Token(TOKEN_TYPES["TROOF"], True),
            "FAIL": Token(TOKEN_TYPES["TROOF"], False),
            "NOOB": Token(TOKEN_TYPES["LITERAL"], None),
        }
        
        while i < len(line):
            char = line[i]
            
            # Handle boolean 
            found_bool = False
            for found_bool, token in BOOLEAN_VALUES.items():
                if line[i:].upper().startswith(found_bool):
                    tokens.append(token)
                    i += len(found_bool)
                    found_bool = True
                    break
            
            if found_bool:
                continue
        
            # Ignore whitespaces
            if char.isspace():
                i += 1
                continue
            
            # Handle strings
            if char == '"':
                string_value = ""
                i += 1  # Skip opening quote
                while i < len(line) and line[i] != '"':
                    string_value += line[i]
                    i += 1
                i += 1  # Skip closing quote
                tokens.append(Token(TOKEN_TYPES["STRING"], string_value))
                continue
            
            # Handle numbers
            if char.isdigit():
                num = ""
                while i < len(line) and (line[i].isdigit() or line[i] == '.'):
                    num += line[i]
                    i += 1
                tokens.append(Token(TOKEN_TYPES["NUMBER"], num))
                continue
            
            # Handle keywords and identifiers
            if char.isalpha():
                word = ""
                while i < len(line) and line[i].isalnum():  # Removed space condition
                    word += line[i]
                    i += 1
                if word in KEYWORDS:
                    tokens.append(Token(TOKEN_TYPES["KEYWORD"], word))
                else:
                    tokens.append(Token(TOKEN_TYPES["IDENTIFIER"], word))
                continue
            
            # Handle operators
            if char in "+-*/=<>!":
                tokens.append(Token(TOKEN_TYPES["OPERATOR"], char))
                i += 1
                continue
            
            # Handle comments
            if char == '#':
                comment = ""
                i += 1
                while i < len(line):
                    comment += line[i]
                    i += 1
                tokens.append(Token(TOKEN_TYPES["COMMENT"], comment))
                continue
            
            i += 1

            """ developer notes:
                need to add handle cases for delimiters, bools, cond statements, etc.
            """
        return tokens