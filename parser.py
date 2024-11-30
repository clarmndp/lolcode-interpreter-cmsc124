from lexer import visible
import re

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
class Parser(object):
    def __init__(self,tokens):
        self.tokens=tokens
        
        self.index=0
    def advance(self):
        self.token_index +=1

        if self.index < len(self.tokens):
            self.current_tok=self.tokens[self.index]
        return self.current_tok
            
        

    def parse(self):
        return self.parse_expression()
    def boolean_expression(self,bool_operation):
        #Should have typecasting to type troof so if the operand is still an expression it must be evaluated first
        if re.search(r"BOTH OF",bool_operation[0][1]):
            if bool_operation[1][1]=="WIN":
                x= 1
            else:
                x=0
            if bool_operation[3][1]=="WIN":
                y=1
            else:
                y=0
            print(f"x{x} y{y}")
            if x and y == 1:
                return (("TROOF","WIN"))
            else:
                return (("TROOF","FAIL"))

        elif re.search(r"EITHER OF", bool_operation[0][1]):
            if bool_operation[1][1]=="WIN":
                x= 1
            else:
                x=0
            if bool_operation[3][1]=="WIN":
                y=1
            else:
                y=0
            if x or y == 1:
                return (("TROOF","WIN"))
            else:
                return (("TROOF","FAIL"))
        
        elif re.search(r"WON OF", bool_operation[0][1]):
            if bool_operation[1][1]=="WIN":
                x= 1
            else:
                x=0
            if bool_operation[3][1]=="WIN":
                y=1
            else:
                y=0
            if x ^ y == 1:
                return (("TROOF","WIN"))
            else:
                return (("TROOF","FAIL"))
        elif re.search(r"NOT", bool_operation[0][1]):
            if bool_operation[1][1]=="WIN":
                x= 1
            else:
                x=0
            if not x==True:
                return (("TROOF","WIN"))
            else:
                return (("TROOF","FAIL"))
    def comparsion(self,comp_exp):

        if re.search(r"BOTH SAEM",comp_exp[0][1]):
            
            if isinstance(comp_exp[3][1],str) and re.search(r"BIGGR OF", comp_exp[3][1]):
                if comp_exp[1] != comp_exp[4]:
                    print("SYNTAX ERROR")
                    exit() #Replace something that can halt the main program
                else:
                    if comp_exp[1][1]>=comp_exp[-1][1]:
                        return ("TROOF", "WIN")
                    else:
                        return ("TROOF", "FAIL")
                    
            elif isinstance(comp_exp[3][1],str) and re.search(r"SMALLR OF", comp_exp[3][1]):
                if comp_exp[1]!= comp_exp[4]:
                    print("SYNTAX ERROR")
                    exit() #Replace something that can halt the main program
                else:
                    if comp_exp[1][1]<=comp_exp[-1][1]:
                        return ("TROOF", "WIN")
                    else:
                        return ("TROOF", "FAIL")
            else:
                
                if comp_exp[1][1]==comp_exp[-1][1]:
                    return ("TROOF", "WIN")
                else:
                    return ("TROOF", "FAIL")
        elif re.search(r"DIFFRINT", comp_exp[0][1]):
            if isinstance(comp_exp[3][1],str) and re.search(r"BIGGR OF", comp_exp[3][1]):
                if comp_exp[1] != comp_exp[4]:
                    print("SYNTAX ERROR")
                    exit() #Replace something that can halt the main program
                else:
                    if comp_exp[1][1]>comp_exp[-1][1]:
                        return ("TROOF", "WIN")
                    else:
                        return ("TROOF", "FAIL")
                    
            elif isinstance(comp_exp[3][1],str) and  re.search(r"SMALLR OF", comp_exp[3][1]):
                if comp_exp[1] != comp_exp[4]:
                    print("SYNTAX ERROR")
                    exit() #Replace something that can halt the main program
                else:
                    if comp_exp[1][1]<comp_exp[-1][1]:
                        return ("TROOF", "WIN")
                    else:
                        return ("TROOF", "FAIL")
            else:
                if comp_exp[1][1]!=comp_exp[-1][1]:
                    return ("TROOF", "WIN")
                else:
                    return ("TROOF", "FAIL")
               
                
    def arithmetic_expression(self,ar_operation):
        print("+++++++++++++++++++++++++++++++++++++++")
        print(ar_operation)
        for i in range(len(ar_operation)-1,-1, -1):
                    
            if not re.search(r"NUMBR",ar_operation[i][0]) and not re.search(r"NUMBAR",ar_operation[i][0])  and re.search(r"SUM OF", ar_operation[i][1]):
                print("Adding")
                # Find the an seperator
                temp_index=i #Holds the index of the AN of that keyword
            
                while 1:
                    if  not re.search(r"NUMBR",ar_operation[temp_index][0]) and not re.search(r"NUMBAR",ar_operation[temp_index][0]) and re.search(r"AN", ar_operation[temp_index][1]):
                        break
                    temp_index+=1
                
                temp_val= ar_operation[temp_index-1][1] + ar_operation[temp_index+1][1]

                if isinstance(temp_val,int):

                    temp_val = ("NUMBR", temp_val)
                else:
                    temp_val = ("NUMBAR",temp_val)
                ar_operation.insert(i,temp_val)
                
                #pop the sum of, left operand , "AN" , and ,right operand
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
                
            elif not re.search(r"NUMBR",ar_operation[i][0])  and not re.search(r"NUMBAR",ar_operation[i][0]) and re.search(r"DIFF OF", ar_operation[i][1]):
                print("SUBTRACTING")
                temp_index=i #Holds the index of the AN of that keyword
               
                while 1:
                    if  not re.search(r"NUMBR",ar_operation[temp_index][0]) and not re.search(r"NUMBAR",ar_operation[temp_index][0]) and re.search(r"AN", ar_operation[temp_index][1]):
                        break
                    temp_index+=1
                temp_val= ar_operation[temp_index-1][1] - ar_operation[temp_index+1][1]
                if isinstance(temp_val,int):

                    temp_val = ("NUMBR", temp_val)
                else:
                    temp_val = ("NUMBAR",temp_val)
                ar_operation.insert(i,temp_val)
                #pop the sum of, left operand , "AN" , and ,right operand
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
            elif not re.search(r"NUMBR",ar_operation[i][0]) and not re.search(r"NUMBAR",ar_operation[i][0]) and re.search(r"PRODUKT OF", ar_operation[i][1]):
                print("MULTIPLYING")
                temp_index=i #Holds the index of the AN of that keyword
               
                while 1:
                    if  not re.search(r"NUMBR",ar_operation[temp_index][0]) and not re.search(r"NUMBAR",ar_operation[temp_index][0]) and re.search(r"AN", ar_operation[temp_index][1]):
                        break
                    temp_index+=1
               
                temp_val= ar_operation[temp_index-1][1] * ar_operation[temp_index+1][1]
                if isinstance(temp_val,int):

                    temp_val = ("NUMBR", temp_val)
                else:
                    temp_val = ("NUMBAR",temp_val)
                ar_operation.insert(i,temp_val)
                #pop the sum of, left operand , "AN" , and ,right operand
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
            elif not re.search(r"NUMBR",ar_operation[i][0]) and not re.search(r"NUMBAR",ar_operation[i][0]) and re.search(r"QUOSHUNT OF", ar_operation[i][1]):
                print("DIVIDING")
                temp_index=i #Holds the index of the AN of that keyword
               
                while 1:
                    if  not re.search(r"NUMBR",ar_operation[temp_index][0]) and not re.search(r"NUMBAR",ar_operation[temp_index][0]) and re.search(r"AN", ar_operation[temp_index][1]):
                        break
                    temp_index+=1
               
                temp_val= ar_operation[temp_index-1][1] / ar_operation[temp_index+1][1]
                if isinstance(temp_val,int):

                    temp_val = ("NUMBR", temp_val)
                else:
                    temp_val = ("NUMBAR",temp_val)
                ar_operation.insert(i,temp_val)
                #pop the sum of, left operand , "AN" , and ,right operand
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
        print(ar_operation)
        return ar_operation[0][1]
    def parse_expression(self):
       
        if re.search(visible, self.tokens[0][1]):
            if re.search(r"STRING", self.tokens[1][0]):
                print("STRING LITERAL")
                print(self.tokens[1][1].strip('"'))
            elif re.search(r"arithmetic_operator", self.tokens[1][0]):
                #Find the last arithmetic opreation
               
                
                temp= self.tokens.copy()
                temp.pop(0) #Pop the visible keyword
                print(f"RESULT: {self.arithmetic_expression(temp)}")
            elif re.search(r"comparison_operator",self.tokens[1][0]):
                temp= self.tokens.copy()
                temp.pop(0) #Pop the visible keyword
                print(temp)
                val= self.comparsion(temp)
                print(val[1])
            elif re.search(r"boolean_operator",self.tokens[1][0]):

                temp= self.tokens.copy()
                temp.pop(0) #Pop the visible keyword
                print(temp)
                val= self.boolean_expression(temp)
                print(val[1])

