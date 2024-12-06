from lexer import visible
import re

declaration_status=0
symbol_table={}
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
    def concat(self,operands):
        if len(operands)<4:
            print("ERROR: Smoosh needs at least two operands")
            exit()
        else:
            operands.pop(0) #pop the keyword
            return_string= ""
            for i in operands:
                if i[1] != "AN":
                    if i[0] != "STRING":
                        print("ERROR: SMOOSH only accepts strings as an operand")
                        exit()
                    else:
                        return_string+=i[1].strip('"')
        return (("STRING", return_string))
    def boolean_expression(self,bool_operation):
        #Should have typecasting to type troof so if the operand is still an expression it must be evaluated first
        if re.search(r"BOTH OF",bool_operation[0][1]):
            if bool_operation[1][0]== "variable":
                if bool_operation[1][1] in symbol_table:
                    x= symbol_table[bool_operation[1][1]]

                    if x!="WIN" and x!="FAIL":
                        print(f"ERROR: Invalid Variable")
                        exit()
                else:
                    print(f"ERROR: Variable {bool_operation[1][1]} does not exist or is not defined")
            else:
                x=bool_operation[1][1]

            if x=="WIN":
                x= 1
            else:
                x=0
            if bool_operation[3][0]== "variable":
                if bool_operation[3][1] in symbol_table:
                    y= symbol_table[bool_operation[3][1]]
                    if y!="WIN" and y!="FAIL":
                        print(f"ERROR: Invalid Variable")
                        exit()
                else:
                    print(f"ERROR: Variable {bool_operation[3][1]} does not exist or is not defined")
            else:
                y=bool_operation[3][1]
            if y=="WIN":
                y=1
            else:
                y=0
            
            if x and y == 1:
                return (("TROOF","WIN"))
            else:
                return (("TROOF","FAIL"))

        elif re.search(r"EITHER OF", bool_operation[0][1]):
            if bool_operation[1][0]== "variable":
                if bool_operation[1][1] in symbol_table:
                    x= symbol_table[bool_operation[1][1]]

                    if x!="WIN" and x!="FAIL":
                        print(f"ERROR: Invalid Variable")
                        exit()
                    print(f"Tesing {bool_operation[1][1]}")
                else:
                    print(f"ERROR: Variable {bool_operation[1][1]} does not exist or is not defined")
            else:
                x=bool_operation[1][1]

            if x=="WIN":
                x= 1
            else:
                x=0
            if bool_operation[3][0]== "variable":
                if bool_operation[3][1] in symbol_table:
                    y= symbol_table[bool_operation[3][1]]
                    if y!="WIN" and y!="FAIL":
                        print(f"ERROR: Invalid Variable")
                        exit()
                else:
                    print(f"ERROR: Variable {bool_operation[3][1]} does not exist or is not defined")
            else:
                y=bool_operation[3][1]
            if y=="WIN":
                y=1
            else:
                y=0
            if x or y == 1:
                return (("TROOF","WIN"))
            else:
                return (("TROOF","FAIL"))
        
        elif re.search(r"WON OF", bool_operation[0][1]):
            if bool_operation[1][0]== "variable":
                if bool_operation[1][1] in symbol_table:
                    x= symbol_table[bool_operation[1][1]]

                    if x!="WIN" and x!="FAIL":
                        print(f"ERROR: Invalid Variable")
                        exit()
                    print(f"Tesing {bool_operation[1][1]}")
                else:
                    print(f"ERROR: Variable {bool_operation[1][1]} does not exist or is not defined")
            else:
                x=bool_operation[1][1]

            if x=="WIN":
                x= 1
            else:
                x=0
            if bool_operation[3][0]== "variable":
                if bool_operation[3][1] in symbol_table:
                    y= symbol_table[bool_operation[3][1]]
                    if y!="WIN" and y!="FAIL":
                        print(f"ERROR: Invalid Variable")
                        exit()
                else:
                    print(f"ERROR: Variable {bool_operation[3][1]} does not exist or is not defined")
            else:
                y=bool_operation[3][1]
            if y=="WIN":
                y=1
            else:
                y=0
            if x ^ y == 1:
                return (("TROOF","WIN"))
            else:
                return (("TROOF","FAIL"))
        elif re.search(r"NOT", bool_operation[0][1]):
            if bool_operation[1][0]== "variable":
                if bool_operation[1][1] in symbol_table:
                    x= symbol_table[bool_operation[1][1]]

                    if x!="WIN" and x!="FAIL":
                        print(f"ERROR: Invalid Variable")
                        exit()
                    print(f"Tesing {bool_operation[1][1]}")
                else:
                    print(f"ERROR: Variable {bool_operation[1][1]} does not exist or is not defined")
            else:
                x=bool_operation[1][1]

            if x=="WIN":
                x= 1
            else:
                x=0
            if not x==True:
                return (("TROOF","WIN"))
            else:
                return (("TROOF","FAIL"))
        elif re.search(r"ALL OF",bool_operation[0][1]):
            if bool_operation[-1][1]!= "MKAY":
                print('ERROR: This operation requires a "MKAY" at the end')
                exit()
            bool_operation.pop(-1)
            result_bool= True
            # CHECKS ALL OPERANDS/ EXPRESSION AND CHECK IF THEY ARE TRUE OR NOT ; IF IT ENCOUNTERS A FALSE IMMEDIATELY RETURN
            for i in range(len(bool_operation)-2,-1,-1):
                #Find the last AN
                if re.search(r"BOTH OF", bool_operation[i][1]) or re.search(r"EITHER OF", bool_operation[i][1]) or re.search(r"WON OF", bool_operation[i][1]) or re.search(r"WON OF", bool_operation[i][1]) :
                       
                    
                    #Call this function again
                    if bool_operation[i][1]== "NOT":
                        temp = self.boolean_expression(bool_operation[i],bool_operation[i+1])
                        print(f"TESTING1 : {temp}")
                        if temp[1] =="WIN":
                            bool_temp = True
                        else:
                            bool_temp=False
                        #Immediately return since if one is false in ALL OF then its false no matter the value of the operands
                        if result_bool and bool_temp == False:
                            return(("TROOF","FAIL"))
                    else:
                        temp = self.boolean_expression([bool_operation[i],bool_operation[i+1],bool_operation[i+2],bool_operation[i+3]])
                        print(f"TESTING : {temp}")
                        if temp[1] =="WIN":
                            bool_temp = True
                        else:
                            bool_temp=False
                        if result_bool and bool_temp == False:
                            return(("TROOF","FAIL"))
                    
            return (("TROOF","WIN"))
        elif re.search(r"ANY OF",bool_operation[0][1]):
            if bool_operation[-1][1]!= "MKAY":
                print('ERROR: This operation requires a "MKAY" at the end')
                exit()
            bool_operation.pop(-1)
            result_bool= False
            # CHECKS ALL OPERANDS/ EXPRESSION AND CHECK IF THEY ARE TRUE OR NOT ; IF IT ENCOUNTERS A FALSE IMMEDIATELY RETURN
            for i in range(len(bool_operation)-2,-1,-1):
                #Find the last AN
                if re.search(r"BOTH OF", bool_operation[i][1]) or re.search(r"EITHER OF", bool_operation[i][1]) or re.search(r"WON OF", bool_operation[i][1]) or re.search(r"WON OF", bool_operation[i][1]) :
                       
                    
                    #Call this function again
                    if bool_operation[i][1]== "NOT":
                        temp = self.boolean_expression(bool_operation[i],bool_operation[i+1])
                        print(f"TESTING1 : {temp}")
                        if temp[1] =="WIN":
                            bool_temp = True
                        else:
                            bool_temp=False
                        #Immediately return since if one is false in ALL OF then its false no matter the value of the operands
                        if result_bool or bool_temp == True:
                            return(("TROOF","WIN"))
                    else:
                        temp = self.boolean_expression([bool_operation[i],bool_operation[i+1],bool_operation[i+2],bool_operation[i+3]])
                        print(f"TESTING : {temp}")
                        if temp[1] =="WIN":
                            bool_temp = True
                        else:
                            bool_temp=False
                        if result_bool or bool_temp == True:
                            return(("TROOF","WIN"))
                    
            return (("TROOF","FAIL"))

    #RETURN TYPE TUPLE OF TROOF, WIN|FAIL
    def comparsion(self,comp_exp):
        
        if re.search(r"BOTH SAEM",comp_exp[0][1]):
            
            
            if isinstance(comp_exp[3][1],str) and re.search(r"BIGGR", comp_exp[3][1]):
                
                if comp_exp[1] != comp_exp[4]:
                    print("SYNTAX ERROR")
                    exit() #Replace something that can halt the main program
                else:
                    if comp_exp[1][0]=="variable":
                        if comp_exp[1][1] in symbol_table:
                            x= symbol_table[comp_exp[1][1]]

                        else:
                            print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
                            exit()

                    else:
                        x=comp_exp[1][1]
                    if comp_exp[6][0]=="variable":
                        if comp_exp[6][1] in symbol_table:
                            y= symbol_table[comp_exp[6][1]]
                            

                        else:
                            print(f"ERROR: Variable {comp_exp[6][1]} does not exist or is not defined")
                            exit()
                    else:
                        y=comp_exp[6][1]
                    if x>=y:
                        return ("TROOF", "WIN")
                    else:
                        return ("TROOF", "FAIL")
                    
            elif isinstance(comp_exp[3][1],str) and re.search(r"SMALLR", comp_exp[3][1]):
               
                if comp_exp[1]!= comp_exp[4]:
                    print("SYNTAX ERROR")
                    exit() #Replace something that can halt the main program
                else:
                    if comp_exp[1][0]=="variable":
                        if comp_exp[1][1] in symbol_table:
                            x= symbol_table[comp_exp[1][1]]

                        else:
                            print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
                            exit()

                    else:
                        x=comp_exp[1][1]
        
                    if comp_exp[6][0]=="variable":
                        if comp_exp[6][1] in symbol_table:
                            y= symbol_table[comp_exp[6][1]]
                        else:
                            print(f"ERROR: Variable {comp_exp[6][1]} does not exist or is not defined")
                            exit()
                    else:
                        y=comp_exp[6][1]
                    if x<=y:
                        return ("TROOF", "WIN")
                    else:
                        return ("TROOF", "FAIL")
            else:
                if comp_exp[1][0]=="variable":
                    if comp_exp[1][1] in symbol_table:
                        x= symbol_table[comp_exp[1][1]]

                    else:
                        print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
                        exit()

                else:
                    x=comp_exp[1][1]
                if comp_exp[3][0]=="variable":
                    if comp_exp[3][1] in symbol_table:
                        y= symbol_table[comp_exp[3][1]]
                        

                    else:
                        print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
                else:
                    y=comp_exp[3][1]
                if x==y:
                    return ("TROOF", "WIN")
                else:
                    return ("TROOF", "FAIL")
        elif re.search(r"DIFFRINT", comp_exp[0][1]):
            if isinstance(comp_exp[3][1],str) and re.search(r"BIGGR", comp_exp[3][1]):
                if comp_exp[1] != comp_exp[4]:
                    print("SYNTAX ERROR")
                    exit() #Replace something that can halt the main program
                else:
                    if comp_exp[1][0]=="variable":
                        if comp_exp[1][1] in symbol_table:
                            x= symbol_table[comp_exp[1][1]]

                        else:
                            print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
                            exit()

                    else:
                        x=comp_exp[1][1]
                    if comp_exp[6][0]=="variable":
                        if comp_exp[6][1] in symbol_table:
                            y= symbol_table[comp_exp[6][1]]
                        else:
                            print(f"ERROR: Variable {comp_exp[6][1]} does not exist or is not defined")
                            exit()
                    else:
                        y=comp_exp[6][1]
                    if x>y:
                        return ("TROOF", "WIN")
                    else:
                        return ("TROOF", "FAIL")
                    
            elif isinstance(comp_exp[3][1],str) and  re.search(r"SMALLR", comp_exp[3][1]):
                if comp_exp[1] != comp_exp[4]:
                    print("SYNTAX ERROR")
                    exit() #Replace something that can halt the main program
                else:
                    if comp_exp[1][0]=="variable":
                        if comp_exp[1][1] in symbol_table:
                            x= symbol_table[comp_exp[1][1]]

                        else:
                            print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
                            exit()

                    else:
                        x=comp_exp[1][1]
        
                    if comp_exp[6][0]=="variable":
                        if comp_exp[6][1] in symbol_table:
                            y= symbol_table[comp_exp[6][1]]
                        else:
                            print(f"ERROR: Variable {comp_exp[6][1]} does not exist or is not defined")
                            exit()
                    else:
                        y=comp_exp[6][1]
                    if x<y:
                        return ("TROOF", "WIN")
                    else:
                        return ("TROOF", "FAIL")
            else:
                
                if comp_exp[1][0]=="variable":
                    if comp_exp[1][1] in symbol_table:
                        x= symbol_table[comp_exp[1][1]]
                    else:
                        print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
                        exit()
                else:
                    x=comp_exp[1][1]
                if comp_exp[3][0]=="variable":
                    if comp_exp[3][1] in symbol_table:
                        y= symbol_table[comp_exp[3][1]]

                    else:
                        print(f"ERROR: Variable {comp_exp[3][1]} does not exist or is not defined")
                else:
                    y=comp_exp[3][1]
                if x!=y:
                    return ("TROOF", "WIN")
                else:
                    return ("TROOF", "FAIL")
               
                
    def arithmetic_expression(self,ar_operation):
        for i in range(len(ar_operation)-1,-1, -1):
                    
            if not re.search(r"NUMBR",ar_operation[i][0]) and not re.search(r"NUMBAR",ar_operation[i][0])  and re.search(r"SUM OF", ar_operation[i][1]):
                print("Adding")
                # Find the an seperator
                temp_index=i #Holds the index of the AN of that keyword
            
                while 1:
                    if  not re.search(r"NUMBR",ar_operation[temp_index][0]) and not re.search(r"NUMBAR",ar_operation[temp_index][0]) and re.search(r"AN", ar_operation[temp_index][1]):
                        break
                    temp_index+=1
                #Evaluate X ; Check if variable or not
                if ar_operation[temp_index-1][0] == "variable":
                    if ar_operation[temp_index-1][1] in symbol_table:
                        x= symbol_table[ar_operation[temp_index-1][1]]
                        if not isinstance(x,float) and not isinstance(x,int):
                            print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                            exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index-1][1]}does not exists")
                else:
                    x = ar_operation[temp_index-1][1]
                if ar_operation[temp_index+1][0] == "variable":
                    if ar_operation[temp_index+1][1] in symbol_table:
                        y= symbol_table[ar_operation[temp_index+1][1]]
                        if not isinstance(y,float) and not isinstance(y,int):
                            print(f"ERROR: Invalid Data type {ar_operation[temp_index+1][1]} must be of data type NUMBR or NUMBAR")
                            exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index+1][1]}does not exists")
                else:
                    y = ar_operation[temp_index+1][1]
                temp_val= x + y
                
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
                #Evaluate X ; Check if variable or not
                if ar_operation[temp_index-1][0] == "variable":
                    if ar_operation[temp_index-1][1] in symbol_table:
                        x= symbol_table[ar_operation[temp_index-1][1]]
                        if not isinstance(x,float) and not isinstance(x,int):
                            print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                            exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index-1][1]}does not exists")
                else:
                    x = ar_operation[temp_index-1][1]
                if ar_operation[temp_index+1][0] == "variable":
                    if ar_operation[temp_index+1][1] in symbol_table:
                        y= symbol_table[ar_operation[temp_index+1][1]]
                        if not isinstance(y,float) and not isinstance(y,int):
                            print(f"ERROR: Invalid Data type {ar_operation[temp_index+1][1]} must be of data type NUMBR or NUMBAR")
                            exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index+1][1]}does not exists")
                else:
                    y = ar_operation[temp_index+1][1]
                temp_val= x-y
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
                #Evaluate X ; Check if variable or not
                if ar_operation[temp_index-1][0] == "variable":
                    if ar_operation[temp_index-1][1] in symbol_table:
                        x= symbol_table[ar_operation[temp_index-1][1]]
                        if not isinstance(x,float) and not isinstance(x,int):
                            print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                            exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index-1][1]}does not exists")
                else:
                    x = ar_operation[temp_index-1][1]
                if ar_operation[temp_index+1][0] == "variable":
                    if ar_operation[temp_index+1][1] in symbol_table:
                        y= symbol_table[ar_operation[temp_index+1][1]]
                        if not isinstance(y,float) and not isinstance(y,int):
                            print(f"ERROR: Invalid Data type {ar_operation[temp_index+1][1]} must be of data type NUMBR or NUMBAR")
                            exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index+1][1]}does not exists")
                else:
                    y = ar_operation[temp_index+1][1]
                temp_val= x*y
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
                #Evaluate X ; Check if variable or not
                if ar_operation[temp_index-1][0] == "variable":
                    if ar_operation[temp_index-1][1] in symbol_table:
                        x= symbol_table[ar_operation[temp_index-1][1]]
                        if not isinstance(x,float) and not isinstance(x,int):
                            print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                            exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index-1][1]}does not exists")
                else:
                    x = ar_operation[temp_index-1][1]
                if ar_operation[temp_index+1][0] == "variable":
                    if ar_operation[temp_index+1][1] in symbol_table:
                        y= symbol_table[ar_operation[temp_index+1][1]]
                        if not isinstance(y,float) and not isinstance(y,int):
                            print(f"ERROR: Invalid Data type {ar_operation[temp_index+1][1]} must be of data type NUMBR or NUMBAR")
                            exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index+1][1]}does not exists")
                else:
                    y = ar_operation[temp_index+1][1]
                temp_val= x/y
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
            #FOR MAX AND MIN IMPLEMENTATION
            elif re.search(r"relational_operation", ar_operation[i][0]):
                #For max() method
                if re.search(r"BIGGR OF",ar_operation[i][1]):
                    temp_index=i
                    print("tesing1232")
                    while 1:
                        if  not re.search(r"NUMBR",ar_operation[temp_index][0]) and not re.search(r"NUMBAR",ar_operation[temp_index][0]) and re.search(r"AN", ar_operation[temp_index][1]):
                            break
                        temp_index+=1
                    
                    #Evaluate X ; Check if variable or not
                    if ar_operation[temp_index-1][0] == "variable":
                        if ar_operation[temp_index-1][1] in symbol_table:
                            x= symbol_table[ar_operation[temp_index-1][1]]
                            if not isinstance(x,float) and not isinstance(x,int):
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                exit()
                        else:
                            print(f"ERROR: Variable {ar_operation[temp_index-1][1]}does not exists")
                    else:
                        x = ar_operation[temp_index-1][1]
                    #Evaluate Y
                    if ar_operation[temp_index+1][0] == "variable":
                        if ar_operation[temp_index+1][1] in symbol_table:
                            y= symbol_table[ar_operation[temp_index+1][1]]
                            if not isinstance(y,float) and not isinstance(y,int):
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index+1][1]} must be of data type NUMBR or NUMBAR")
                                exit()
                        else:
                            print(f"ERROR: Variable {ar_operation[temp_index+1][1]}does not exists")
                    else:
                        y = ar_operation[temp_index+1][1]
                    temp_val= max(x,y)
                    if isinstance(temp_val,int):

                        temp_val = ("NUMBR", temp_val)
                    else:
                        temp_val = ("NUMBAR",temp_val)
                    ar_operation.insert(i,temp_val)
                    #pop the BIGGR OF, left operand , "AN" , and ,right operand
                    ar_operation.pop(i+1)
                    ar_operation.pop(i+1)
                    ar_operation.pop(i+1)
                    ar_operation.pop(i+1)
                #Minimum
                elif re.search(r"SMALLR OF",ar_operation[i][1]):
                    temp_index=i
                    print("tesing1232")
                    while 1:
                        if  not re.search(r"NUMBR",ar_operation[temp_index][0]) and not re.search(r"NUMBAR",ar_operation[temp_index][0]) and re.search(r"AN", ar_operation[temp_index][1]):
                            break
                        temp_index+=1
                    
                    #Evaluate X ; Check if variable or not
                    if ar_operation[temp_index-1][0] == "variable":
                        if ar_operation[temp_index-1][1] in symbol_table:
                            x= symbol_table[ar_operation[temp_index-1][1]]
                            if not isinstance(x,float) and not isinstance(x,int):
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                exit()
                        else:
                            print(f"ERROR: Variable {ar_operation[temp_index-1][1]}does not exists")
                    else:
                        x = ar_operation[temp_index-1][1]
                    #Evaluate Y
                    if ar_operation[temp_index+1][0] == "variable":
                        if ar_operation[temp_index+1][1] in symbol_table:
                            y= symbol_table[ar_operation[temp_index+1][1]]
                            if not isinstance(y,float) and not isinstance(y,int):
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index+1][1]} must be of data type NUMBR or NUMBAR")
                                exit()
                        else:
                            print(f"ERROR: Variable {ar_operation[temp_index+1][1]}does not exists")
                    else:
                        y = ar_operation[temp_index+1][1]
                    temp_val= min(x,y)
                    if isinstance(temp_val,int):

                        temp_val = ("NUMBR", temp_val)
                    else:
                        temp_val = ("NUMBAR",temp_val)
                    ar_operation.insert(i,temp_val)
                    #pop the BIGGR OF, left operand , "AN" , and ,right operand
                    ar_operation.pop(i+1)
                    ar_operation.pop(i+1)
                    ar_operation.pop(i+1)
                    ar_operation.pop(i+1)

        print(ar_operation)
        return ar_operation[0][1]
    def check_varname(self,varname):
        pattern= r"[A-Za-z][A-Za-z\d]*"
        if re.search(pattern, varname):
            return True
        else:
            return False
    def parse_expression(self):
        global declaration_status
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
            elif re.search(r"concatenation", self.tokens[1][0]):
                temp= self.tokens.copy()
                temp.pop(0)
                val = self.concat(temp)
                print(val[1])
            elif re.search(r"variable",self.tokens[1][0]):
                if self.tokens[1][1] in symbol_table:
                    print(symbol_table[self.tokens[1][1]])
                else:
                    print(f"ERROR: Variable {self.tokens[1][1]} does not exist or is not defined")
                   
        if re.search(r"declaration_start", self.tokens[0][0]):
            declaration_status+=1
               
        if re.search(r"declaration_end",self.tokens[0][0]):
            declaration_status+=1
        #DECLARATION
        if re.search(r"declaration_keyword",self.tokens[0][0]):
            if declaration_status>1:
                print("ERROR: Declare this variable inside the  WAZZUP-BUHBYE section")
                exit()
            else:
                if len(self.tokens)==2:
                    #Check if valid variable name
                    if self.check_varname(self.tokens[1][1]):
                        symbol_table[self.tokens[1][1]]= None
                    else:
                        print("ERROR: Invalid Variable name")
                        exit()
                else:
                    if self.check_varname(self.tokens[1][1]):
                        temp1= self.tokens.copy() #Copy the token
                        temp1.pop(0) #Pop the I HAS A
                        varname = temp1.pop(0) #Put it into a temp variable and pop the varname
                        temp1.pop(0) # Pop ITZ
                        print(f"Varname {varname[1]}")
                        print(temp1) 
                        #Evaluate the expression
                        if re.search(r"STRING",temp1[0][0]):
                            
                            symbol_table[varname[1]]=temp1[0][1].strip('"')
                        elif re.search(r"TROOF",temp1[0][0]):
                            print("testi")
                            symbol_table[varname[1]]=temp1[0][1]
                        elif re.search(r"NUMBR", temp1[0][0]):
                            symbol_table[varname[1]]= temp1[0][1]
                        elif re.search(r"NUMBAR", temp1[0][0]):
                            symbol_table[varname[1]]= temp1[0][1]
                        elif re.search(r"arithmetic_operator", temp1[0][0]):                       
                            temp= temp1.copy()
                            print(f"RESULT: {self.arithmetic_expression(temp)}")
                            # result=self.arithmetic_expression(temp)
                            # print(result)
                            print(varname[1])
                            symbol_table[varname[1]]=self.arithmetic_expression(temp)
                            print(f"SYMBOL TABLE {symbol_table}")
                        elif re.search(r"comparison_operator",temp1[0][0]):
                            temp= temp1.copy()
                            
                            val= self.comparsion(temp)
                            symbol_table[varname[1]]= val[1]
                        elif re.search(r"boolean_operator",temp1[0][0]):
                            temp= temp1.copy()
    
                            print(temp)
                            val= self.boolean_expression(temp)
                            symbol_table[varname[1]]= val[1]
                        elif re.search(r"concatenation",temp1[0][0]):
                            
                            temp= temp1.copy()
                            val = self.concat(temp)
                            symbol_table[varname[1]]= val[1]
                                
                    else:
                        print("ERROR: Invalid Variable name")
        if re.search(r"variable",self.tokens[0][0]) and re.search((r"reassignment_delimeter"),self.tokens[1][0]):
            if len(self.tokens)>2:
                if self.tokens[0][1] in symbol_table:
                    temp1= self.tokens.copy() #Copy the token
        
                    varname = temp1.pop(0) #Put it into a temp variable and pop the varname
                    temp1.pop(0) # Pop R
                    print(f"Varname {varname[1]}")
                    print(temp1) 
                    #Evaluate the expression
                    if re.search(r"STRING",temp1[0][0]):
                        
                        symbol_table[varname[1]]=temp1[0][1].strip('"')
                    elif re.search(r"TROOF",temp1[0][0]):
                        print("testi")
                        symbol_table[varname[1]]=temp1[0][1]
                    elif re.search(r"NUMBR", temp1[0][0]):
                        symbol_table[varname[1]]= temp1[0][1]
                    elif re.search(r"NUMBAR", temp1[0][0]):
                        symbol_table[varname[1]]= temp1[0][1]
                    elif re.search(r"arithmetic_operator", temp1[0][0]):                       
                        temp= temp1.copy()
                        print(f"RESULT: {self.arithmetic_expression(temp)}")
                        # result=self.arithmetic_expression(temp)
                        # print(result)
                        print(varname[1])
                        symbol_table[varname[1]]=self.arithmetic_expression(temp)
                        print(f"SYMBOL TABLE {symbol_table}")
                    elif re.search(r"comparison_operator",temp1[0][0]):
                        temp= temp1.copy()
                        
                        val= self.comparsion(temp)
                        symbol_table[varname[1]]= val[1]
                    elif re.search(r"boolean_operator",temp1[0][0]):
                        temp= temp1.copy()

                        print(temp)
                        val= self.boolean_expression(temp)
                        symbol_table[varname[1]]= val[1]
                    elif re.search(r"concatenation",temp1[0][0]):
                        
                        temp= temp1.copy()
                        val = self.concat(temp)
                        symbol_table[varname[1]]= val[1]
                else:
                    print("ERROR: Invalid Variable name")
                    exit()
            else:
                print("ERROR: Missing Argument")
                exit()
        


            