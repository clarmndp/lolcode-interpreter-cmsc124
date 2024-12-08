# We define token types for lexical analysis
import re
string_lit =  r'"[^"]*"'
numbr= r"-?\d+"
numbar= r"-?\d*(\.)\d+"
addition= r"SUM OF"
subtraction = r"DIFF OF"
multiplication = r"PRODUKT OF"
division= r"QUOSHUNT OF"
space= r"[\s]"
an= r"AN"
equal= r"R"
visible= r"VISIBLE"
varname =r"[A-Za-z][A-Za-z\d]*"
multiline_comment_flag=0
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
keyword= ["SUM OF", "VISIBLE","+", "DIFF OF","PRODUKT OF", "QUOSHUNT OF",
          "BOTH SAEM", "DIFFRINT", "BIGGR OF", "SMALLR OF","MOD OF",
          "BOTH OF", "EITHER OF", "WON OF", "NOT","WIN","FAIL", "ALL OF","MKAY","ANY OF",
          "I HAS A", "ITZ","WAZZUP","BUHBYE",
          "SMOOSH",
          "R","MAEK A","IS NOW A",
          "GIMMEH",
          "O RLY?", "YA RLY", "NO WAI","OIC",
          "WTF?","OMGWTF", "OMG","GTFO",
          "IM IN YR","UPPIN","NERFIN", "TIL","WILE",
          "OBTW","BTW", "TLDR", 
          ]

class Token:
    """ Parameter 'type' provides the category for TOKEN_TYPES
        Parameter 'value' holds the text/ content
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:  
    # We convert source code by line into tokens
    def definer(line):
        tokens = []
        # Boolean keywords  
        BOOLEAN_VALUES = {
            "WIN": Token(TOKEN_TYPES["TROOF"], True),
            "FAIL": Token(TOKEN_TYPES["TROOF"], False),
            "NOOB": Token(TOKEN_TYPES["LITERAL"], None),
        }
        # token_elem=r'|'.join([re.escape(keyword_elem) for keyword_elem in keyword]) + r'|\S+' # Seperate by space
        token_elem =  r'|'.join([re.escape(keyword_elem) for keyword_elem in keyword]) +r'|'+r'"[^"]*"|\S+'+r'|' +r"-?\d+"+r'|'+r'\S+'
        token_elem=re.findall(token_elem,line)
        # print(token_elem)
        global multiline_comment_flag
        for temp_str in token_elem:
            if temp_str == "KTHXBYE":
                
                tokens.append(("end", temp_str.strip()))
            
            elif re.search(visible, temp_str):
                tokens.append(("expression", temp_str.strip()))
                
            elif re.search(string_lit, temp_str):
               
                tokens.append((TOKEN_TYPES["STRING"],temp_str.strip('"')))
                
            elif re.search(addition,temp_str):
                tokens.append(("arithmetic_operator",temp_str.strip()))
                
            elif re.search(subtraction,temp_str):
                tokens.append(("arithmetic_operator",temp_str.strip()))
               
            elif re.search(division,temp_str):
                tokens.append(("arithmetic_operator",temp_str.strip()))
                
            elif re.search(multiplication,temp_str):
                tokens.append(("arithmetic_operator",temp_str.strip()))
            elif re.search(r"OBTW",temp_str):
                multiline_comment_flag=1
                print("TESTING")
            elif re.search(r"BTW",temp_str):
                return tokens
            elif re.search(r"TLDR",temp_str):
                multiline_comment_flag=0
                if len(tokens)>0:
                    print("ERROR: MULTILINE COMMENT DELIMETER SHOULD NOT BE IN THESAME LINE AS AN ACTUAL CODE")
                    exit()
            elif re.search(r"MOD OF",temp_str):
                tokens.append(("arithmetic_operator",temp_str))
            elif re.search(r"BOTH SAEM", temp_str):
                tokens.append(("comparison_operator",temp_str))
            elif re.search(r"DIFFRINT", temp_str):
                tokens.append(("comparison_operator",temp_str))
            elif re.search(r"BOTH OF", temp_str):
                tokens.append(("boolean_operator",temp_str))
            elif re.search(r"EITHER OF", temp_str):
                tokens.append(("boolean_operator",temp_str))
            elif re.search(r"WON OF", temp_str):
                tokens.append(("boolean_operator",temp_str))
            elif re.search(r"NOT", temp_str):
                tokens.append(("boolean_operator",temp_str))
            elif re.search(r"ALL OF",temp_str):
                tokens.append(("boolean_operator",temp_str))
            elif re.search(r"ANY OF",temp_str):
                tokens.append(("boolean_operator",temp_str))
            elif re.search(r"MKAY", temp_str):
                tokens.append(("inf_arity_delimeter",temp_str))
            elif re.search(r"BIGGR OF", temp_str):
                tokens.append(("arithmetic_operator",temp_str))
            elif re.search(r"SMALLR OF", temp_str):
                tokens.append(("arithmetic_operator",temp_str)) 
            elif re.search(an,temp_str):
                tokens.append(("delimeter", temp_str))
            elif re.search(r"WAZZUP",temp_str):
                tokens.append(("declaration_start", temp_str))
            elif re.search(r"BUHBYE",temp_str):
                tokens.append(("declaration_end", temp_str))
            elif re.search(r"I HAS A",temp_str):
                tokens.append(("declaration_keyword", temp_str))
            elif re.search(r"ITZ",temp_str):
                tokens.append(("declaration_delimiter", temp_str))
            elif re.search(r"WIN", temp_str):
                tokens.append((TOKEN_TYPES["TROOF"],"WIN"))
            elif re.search(r"FAIL", temp_str):
                tokens.append((TOKEN_TYPES["TROOF"],"FAIL"))
            
            elif re.search(r"SMOOSH", temp_str):
                tokens.append(("concatenation", temp_str))
           
            elif re.search(r"MAEK A", temp_str):
                tokens.append(("typecasting_delimeter",temp_str))
            elif re.search(r"IS NOW A", temp_str):
                tokens.append(("typecasting_delimeter",temp_str))
            elif re.search(r"O RLY\?",temp_str):
                tokens.append(("conidtional_start_delimeter",temp_str))
            elif re.search(r"YA RLY",temp_str):
                tokens.append(("conidtional_true",temp_str))
            elif re.search(r"NO WAI",temp_str):
                tokens.append(("conidtional_false",temp_str))
            elif re.search(r"OMGWTF",temp_str):
                tokens.append(("switch_else",temp_str))
            elif re.search(r"WTF\?",temp_str):
                tokens.append(("switch_start_delimeter",temp_str))
            elif re.search(r"OMG",temp_str):
                tokens.append(("switch_case",temp_str))
            elif re.search(r"GTFO",temp_str):
                tokens.append(("switch_break",temp_str))
            elif re.search(r"OIC",temp_str):
                tokens.append(("conidtional_end_delimeter",temp_str))
            elif re.search(r"GIMMEH", temp_str):
                tokens.append(("input", temp_str))
            elif re.search(r"R",temp_str):
                tokens.append(("reassignment_delimeter",temp_str))
            elif re.search(r"\+", temp_str):
                tokens.append(("visible_concat", temp_str))
            elif re.search(varname,temp_str):
                tokens.append(("variable", temp_str))
            elif re.fullmatch(numbar,temp_str):
                tokens.append((TOKEN_TYPES["NUMBAR"], float(temp_str)))
            elif re.fullmatch(numbr,temp_str):
                tokens.append((TOKEN_TYPES["NUMBR"], int(temp_str)))
           
            

                
    
            

        """ developer notes:
            need to add handle cases for delimiters, bools, cond statements, etc.
        """
        # print(tokens)
        if multiline_comment_flag!=0:
            return None
        else:
            return tokens