from lexer import visible
import main
import re

declaration_status=0
symbol_table={}
symbol_table["IT"]=""
ifelse_flag=1
class Node:
    def __init__(self, value, left=None, right=None):
        
        self.value = value
        self.left = left
        self.right = right
class Parser(object):
    def __init__(self,tokens,lexeme_table,index):
        self.index=index
        self.lexeme_table=lexeme_table
        self.tokens=tokens
        
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
                        if i[0] =='variable' and i[1] in symbol_table:
                            return_string+=symbol_table[i[1]].strip('"')
                        else:
                            print("ERROR: SMOOSH only accepts strings as an operand")
                            exit()
                    else:
                        return_string+=i[1].strip('"')
        return (("STRING", return_string))
    def boolean_expression(self,bool_operation):

        if bool_operation[0][1]== "ANY OF":
            if bool_operation[-1][1]!= "MKAY":
                print('ERROR: This operation requires a "MKAY" at the end')
                exit()
            bool_operation.pop(-1)
            result_bool= False
            
            #Evaluate all non variables or a troof
            for i in range(len(bool_operation)-1,-1,-1):
                #CHECKING IF AN ANY OF OR ALL OF operator is found
                
                if ((bool_operation[i][1]=="ANY OF" or bool_operation[i][1]=="ALL OF") and i!=0):
                    print("ERROR: Does not accept ANY OF or ALL OF as an operand")
                    exit()
                if  bool_operation[i][1]=="EITHER OF" or bool_operation[i][1]=="BOTH OF" or bool_operation[i][1]=="WON OF": # 2 operands
                    temp=self.boolean_expression([bool_operation[i], bool_operation[i+1],bool_operation[i+2],bool_operation[i+3]])
                    temp=temp[1]
                    if (isinstance(temp, int) or (isinstance(temp,float))) and temp>0:
                        temp=True
                    elif (isinstance(temp, int) or (isinstance(temp,float))) and temp<0:
                        temp=False
                    elif temp=="WIN":
                        temp=True
                    elif temp=="FAIL":
                        temp=False 
                
                    if temp==False:
                        return(("TROOF","FAIL"))
                    bool_operation.insert(i, ("TROOF", "WIN"))
                    bool_operation.pop(i+1) #Pop the keyword
                    bool_operation.pop(i+1) #Pop the variable
                    bool_operation.pop(i+1) #Pop the an
                    bool_operation.pop(i+1) #Pop the variable
                elif bool_operation[i][1]=="NOT":
                    
                    temp=self.boolean_expression([bool_operation[i], bool_operation[i+1]])
                    temp=temp[1]
                    if (isinstance(temp, int)) and temp==1:
                        temp=True
                    elif (isinstance(temp, int)) and temp==0:
                        temp=False
                    elif temp=="WIN":
                        temp=True
                    elif temp=="FAIL":
                        temp=False 
                    print(f"NOT {temp}")
                    if temp==True:
                        return(("TROOF","WIN"))
                    bool_operation.insert(i, ("TROOF", "FAIL"))
                    bool_operation.pop(i+1) #Pop the NOT
                    bool_operation.pop(i+1) #Pop the variable
                            
            
            bool_operation.pop(0) #POP ANY OF
            #NOW THAT bool_operation is only variable or a troof or a numbr or numbr
            for i in bool_operation:
                
                if i[0]=="TROOF":
                    if i[1]=="FAIL":
                        return(("TROOF","FAIL"))
                elif i[0] == 'variable':
                    if i[1] in symbol_table:
                        temp = symbol_table[i[1]]
                        
                        if temp=="WIN" or  ((isinstance(temp,int) or isinstance(temp,float)) and temp==1):
                            return(("TROOF","WIN"))
                    else:
                        print(f"ERROR: Variable {i[1]} does not exist or is not defined")
            
            return (("TROOF","FAIL")) #NO TRUE DETECTED RETURN WIN
        elif bool_operation[0][1]== "ALL OF":
            if bool_operation[-1][1]!= "MKAY":
                print('ERROR: This operation requires a "MKAY" at the end')
                exit()
            bool_operation.pop(-1)
            
            #Evaluate all non variables or a troof
            for i in range(len(bool_operation)-1,-1,-1):
                #CHECKING IF AN ANY OF OR ALL OF operator is found
                
                if ((bool_operation[i][1]=="ANY OF" or bool_operation[i][1]=="ALL OF") and i!=0):
                    print("ERROR: Does not accept ANY OF or ALL OF as an operand")
                    exit()
                if  bool_operation[i][1]=="EITHER OF" or bool_operation[i][1]=="BOTH OF" or bool_operation[i][1]=="WON OF": # 2 operands
                    temp=self.boolean_expression([bool_operation[i], bool_operation[i+1],bool_operation[i+2],bool_operation[i+3]])
                    temp=temp[1]
                    if (isinstance(temp, int) or (isinstance(temp,float))) and temp<0:
                        temp=False
                    elif (isinstance(temp, int) or (isinstance(temp,float))) and temp>0:
                        temp=True
                    elif temp=="WIN":
                        temp=True
                    elif temp=="FAIL":
                        temp=False 
                
                    if temp=="WIN" or temp==True:
                        return(("TROOF","WIN"))
                    bool_operation.insert(i, ("TROOF", "FAIL"))
                    bool_operation.pop(i+1) #Pop the keyword
                    bool_operation.pop(i+1) #Pop the variable
                    bool_operation.pop(i+1) #Pop the an
                    bool_operation.pop(i+1) #Pop the variable
                elif bool_operation[i][1]=="NOT":
                    
                    temp=self.boolean_expression([bool_operation[i], bool_operation[i+1]])
                    temp=temp[1]
                    if (isinstance(temp, int) or (isinstance(temp,float))) and temp==1:
                        temp=True
                    elif (isinstance(temp, int) or (isinstance(temp,float))) and temp==0:
                        temp=False
                    elif temp=="WIN":
                        temp=True
                    elif temp=="FAIL":
                        temp=False 
                    print(f"NOT {temp}")
                    if temp==False:
                        return(("TROOF","FAIL"))
                    
                    bool_operation.insert(i, ("TROOF", "WIN"))
                    bool_operation.pop(i+1) #Pop the NOT
                    bool_operation.pop(i+1) #Pop the variable
                            
            
            bool_operation.pop(0) #POP ANY OF
            #NOW THAT bool_operation is only variable or a troof or a numbr or numbr
            for i in bool_operation:
                print(i)
                if i[0]=="TROOF":
                    if i[1]=="WIN":
                        return(("TROOF","WIN"))
                elif i[0] == 'variable':
                    if i[1] in symbol_table:
                        temp = symbol_table[i[1]]
                        
                        if temp=="FAIL" or  ((isinstance(temp,int) or isinstance(temp,float)) and temp==0):
                            return(("TROOF","FAIL"))
                    else:
                        print(f"ERROR: Variable {i[1]} does not exist or is not defined")
            return (("TROOF","WIN"))
        elif bool_operation[0][1]== "BOTH OF" or bool_operation[0][1]== "EITHER OF" or bool_operation[0][1]== "WON OF" or bool_operation[0][1]== "NOT":

            for i in range (len(bool_operation)-1,-1,-1):     
                if bool_operation[i][1]=="BOTH OF":
                    if bool_operation[i+1][0]== "variable":
                        if(bool_operation[i+1][1] in symbol_table):
                            x= symbol_table[bool_operation[i+1][1]]
                            if x!="WIN" and x!="FAIL":
                                #CHeck if can be typecasted
                                if isinstance(x, str) and x.isdigit():
                                    x= int(x)
                                    if x>0:
                                        x="WIN"
                                    else:
                                        x="FAIL"
                                else:
                                    try:
                                        x=float(x)
                                    except ValueError:
                                        print(f"ERROR: Operand should be of type TROOF or can be typcasted to one")
                        else:
                            print(f"ERROR: Variable {bool_operation[i+1][1]} does not exist or is not defined")
                    else:
                        x=bool_operation[i+1][1]
                    if bool_operation[i+3][0]== "variable":
                        if(bool_operation[i+3][1] in symbol_table):
                            y= symbol_table[bool_operation[i+3][1]]
                            if y!="WIN" and y!="FAIL":
                                #CHeck if can be typecasted
                                if isinstance(y, str) and y.isdigit():
                                    y= int(y)
                                    if y>0:
                                        y="WIN"
                                    else:
                                        y="FAIL"
                                else:
                                    try:
                                        y=float(y)
                                    except ValueError:
                                        print(f"ERROR: Operand should be of type TROOF or can be typcasted to one")
                        else:
                            print(f"ERROR: Variable {bool_operation[i+3][1]} does not exist or is not defined")
                    else:
                        y=bool_operation[i+3][1]
                        
                    if x=="WIN" or ((isinstance(x,int) or isinstance(x,float)) and x>0):
                        x=True
                    elif x=="FAIL" or  ((isinstance(x,int) or isinstance(x,float)) and x<0):
                        x=False
                    if y== "WIN" or ((isinstance(y,int) or isinstance(y,float)) and y>0):
                        y=True
                    elif y=="FAIL" or ((isinstance(y,int) or isinstance(y,float)) and y<0):
                        y= False
                    
                    if x and y == 1:
                        
                        bool_operation.insert(i, ("TROOF", "WIN"))
                        bool_operation.pop(i+1) #Pops both of
                        bool_operation.pop(i+1) #Pops variable
                        bool_operation.pop(i+1) #Pops an
                        bool_operation.pop(i+1) #Pops variable
                    else:

                        bool_operation.insert(i, ("TROOF", "FAIL"))
                        bool_operation.pop(i+1) #Pops both of
                        bool_operation.pop(i+1) #Pops variable
                        bool_operation.pop(i+1) #Pops an
                        bool_operation.pop(i+1) #Pops variable
                elif bool_operation[i][1] == "EITHER OF":
                    if bool_operation[i+1][0]== "variable":
                        if(bool_operation[i+1][1] in symbol_table):
                            x= symbol_table[bool_operation[i+1][1]]
                            if x!="WIN" and x!="FAIL":
                                #CHeck if can be typecasted
                                if isinstance(x, str) and x.isdigit():
                                    x= int(x)
                                    if x>0:
                                        x="WIN"
                                    else:
                                        x="FAIL"
                                else:
                                    try:
                                        x=float(x)
                                    except ValueError:
                                        print(f"ERROR: Operand should be of type TROOF or can be typcasted to one")
                        else:
                            print(f"ERROR: Variable {bool_operation[i+1][1]} does not exist or is not defined")
                    else:
                        x=bool_operation[i+1][1]
                    if bool_operation[i+3][0]== "variable":
                        if(bool_operation[i+3][1] in symbol_table):
                            y= symbol_table[bool_operation[i+3][1]]
                            if y!="WIN" and y!="FAIL":
                                #CHeck if can be typecasted
                                if isinstance(y, str) and y.isdigit():
                                    y= int(y)
                                    if y>0:
                                        y="WIN"
                                    else:
                                        y="FAIL"
                                else:
                                    try:
                                        y=float(y)
                                    except ValueError:
                                        print(f"ERROR: Operand should be of type TROOF or can be typcasted to one")
                        else:
                            print(f"ERROR: Variable {bool_operation[i+3][1]} does not exist or is not defined")
                    else:
                        y=bool_operation[i+3][1]
                        
                    if x=="WIN" or ((isinstance(x,int) or isinstance(x,float)) and x>0):
                        x=True
                    elif x=="FAIL" or  ((isinstance(x,int) or isinstance(x,float)) and x<0):
                        x=False
                    if y== "WIN" or ((isinstance(y,int) or isinstance(y,float)) and y>0):
                        y=True
                    elif y=="FAIL" or ((isinstance(y,int) or isinstance(y,float)) and y<0):
                        y= False
                    if x or y == 1:
                        
                        bool_operation.insert(i, ("TROOF", "WIN"))
                        bool_operation.pop(i+1) #Pops both of
                        bool_operation.pop(i+1) #Pops variable
                        bool_operation.pop(i+1) #Pops an
                        bool_operation.pop(i+1) #Pops variable
                    else:

                        bool_operation.insert(i, ("TROOF", "FAIL"))
                        bool_operation.pop(i+1) #Pops EITHER of
                        bool_operation.pop(i+1) #Pops variable
                        bool_operation.pop(i+1) #Pops an
                        bool_operation.pop(i+1) #Pops variable
                elif bool_operation[i][1]=="NOT":
                    if bool_operation[i+1][0]== "variable":
                        if(bool_operation[i+1][1] in symbol_table):
                            x= symbol_table[bool_operation[i+1][1]]
                            if x!="WIN" and x!="FAIL":
                                #CHeck if can be typecasted
                                if isinstance(x, str) and x.isdigit():
                                    x= int(x)
                                    if x>0:
                                        x="WIN"
                                    else:
                                        x="FAIL"
                                else:
                                    try:
                                        x=float(x)
                                    except ValueError:
                                        print(f"ERROR: Operand should be of type TROOF or can be typcasted to one")
                        else:
                            print(f"ERROR: Variable {bool_operation[i+1][1]} does not exist or is not defined")
                    else:
                        x=bool_operation[i+1][1]
                    if x=="WIN" or ((isinstance(x,int) or isinstance(x,float)) and x>0):
                        x=True
                    elif x=="FAIL" or  ((isinstance(x,int) or isinstance(x,float)) and x<0):
                        x=False
                    if not x == True:
                        bool_operation.insert(i, ("TROOF", "WIN"))
                        bool_operation.pop(i+1) #Pop the NOT 
                        bool_operation.pop(i+1) # Pop the Variable
                    elif not x == False:
                        bool_operation.insert(i, ("TROOF", "FAIL"))
                        bool_operation.pop(i+1) #Pop the NOT 
                        bool_operation.pop(i+1)
                elif bool_operation[i][1] == "WON OF":
                    if bool_operation[i+1][0]== "variable":
                        if(bool_operation[i+1][1] in symbol_table):
                            x= symbol_table[bool_operation[i+1][1]]
                            if x!="WIN" and x!="FAIL":
                                #CHeck if can be typecasted
                                if isinstance(x, str) and x.isdigit():
                                    x= int(x)
                                    if x>0:
                                        x="WIN"
                                    else:
                                        x="FAIL"
                                else:
                                    try:
                                        x=float(x)
                                    except ValueError:
                                        print(f"ERROR: Operand should be of type TROOF or can be typcasted to one")
                        else:
                            print(f"ERROR: Variable {bool_operation[i+1][1]} does not exist or is not defined")
                    else:
                        x=bool_operation[i+1][1]
                    if bool_operation[i+3][0]== "variable":
                        if(bool_operation[i+3][1] in symbol_table):
                            y= symbol_table[bool_operation[i+3][1]]
                            if y!="WIN" and y!="FAIL":
                                #CHeck if can be typecasted
                                if isinstance(y, str) and y.isdigit():
                                    y= int(y)
                                    if y>0:
                                        y="WIN"
                                    else:
                                        y="FAIL"
                                else:
                                    try:
                                        y=float(y)
                                    except ValueError:
                                        print(f"ERROR: Operand should be of type TROOF or can be typcasted to one")
                        else:
                            print(f"ERROR: Variable {bool_operation[i+3][1]} does not exist or is not defined")
                    else:
                        y=bool_operation[i+3][1]
                        
                    if x=="WIN" or ((isinstance(x,int) or isinstance(x,float)) and x>0):
                        x=True
                    elif x=="FAIL" or  ((isinstance(x,int) or isinstance(x,float)) and x<0):
                        x=False
                    if y== "WIN" or ((isinstance(y,int) or isinstance(y,float)) and y>0):
                        y=True
                    elif y=="FAIL" or ((isinstance(y,int) or isinstance(y,float)) and y<0):
                        y= False
                    if x ^ y == 1:
                        
                        bool_operation.insert(i, ("TROOF", "WIN"))
                        bool_operation.pop(i+1) #Pops both of
                        bool_operation.pop(i+1) #Pops variable
                        bool_operation.pop(i+1) #Pops an
                        bool_operation.pop(i+1) #Pops variable
                    else:

                        bool_operation.insert(i, ("TROOF", "FAIL"))
                        bool_operation.pop(i+1) #Pops EITHER of
                        bool_operation.pop(i+1) #Pops variable
                        bool_operation.pop(i+1) #Pops an
                        bool_operation.pop(i+1) #Pops variable
                
            print(bool_operation)
            return (bool_operation[0])
           

        # #Should have typecasting to type troof so if the operand is still an expression it must be evaluated first
        # if re.search(r"BOTH OF",bool_operation[0][1]):
        #     if bool_operation[1][0]== "variable":
        #         if bool_operation[1][1] in symbol_table:
        #             x= symbol_table[bool_operation[1][1]]

        #             if x!="WIN" and x!="FAIL":
        #                 print(f"ERROR: Invalid Variable")
        #                 exit()
        #         else:
        #             print(f"ERROR: Variable {bool_operation[1][1]} does not exist or is not defined")
        #     else:
        #         x=bool_operation[1][1]

        #     if x=="WIN":
        #         x= 1
        #     else:
        #         x=0
        #     if bool_operation[3][0]== "variable":
        #         if bool_operation[3][1] in symbol_table:
        #             y= symbol_table[bool_operation[3][1]]
        #             if y!="WIN" and y!="FAIL":
        #                 print(f"ERROR: Invalid Variable")
        #                 exit()
        #         else:
        #             print(f"ERROR: Variable {bool_operation[3][1]} does not exist or is not defined")
        #     else:
        #         y=bool_operation[3][1]
        #     if y=="WIN":
        #         y=1
        #     else:
        #         y=0
            
        #     if x and y == 1:
        #         return (("TROOF","WIN"))
        #     else:
        #         return (("TROOF","FAIL"))

        # elif re.search(r"EITHER OF", bool_operation[0][1]):
        #     if bool_operation[1][0]== "variable":
        #         if bool_operation[1][1] in symbol_table:
        #             x= symbol_table[bool_operation[1][1]]

        #             if x!="WIN" and x!="FAIL":
        #                 print(f"ERROR: Invalid Variable")
        #                 exit()
                    
        #         else:
        #             print(f"ERROR: Variable {bool_operation[1][1]} does not exist or is not defined")
        #     else:
        #         x=bool_operation[1][1]

        #     if x=="WIN":
        #         x= 1
        #     else:
        #         x=0
        #     if bool_operation[3][0]== "variable":
        #         if bool_operation[3][1] in symbol_table:
        #             y= symbol_table[bool_operation[3][1]]
        #             if y!="WIN" and y!="FAIL":
        #                 print(f"ERROR: Invalid Variable")
        #                 exit()
        #         else:
        #             print(f"ERROR: Variable {bool_operation[3][1]} does not exist or is not defined")
        #     else:
        #         y=bool_operation[3][1]
        #     if y=="WIN":
        #         y=1
        #     else:
        #         y=0
        #     print(f"xP{bool_operation[1][1]} or y{bool_operation[3][1]}")
        #     print(f"xP{x} or y{y}")
        #     if x or y == 1:
        #         return (("TROOF","WIN"))
        #     else:
        #         return (("TROOF","FAIL"))
        
        # elif re.search(r"WON OF", bool_operation[0][1]):
        #     if bool_operation[1][0]== "variable":
        #         if bool_operation[1][1] in symbol_table:
        #             x= symbol_table[bool_operation[1][1]]

        #             if x!="WIN" and x!="FAIL":
        #                 print(f"ERROR: Invalid Variable")
        #                 exit()
                    
        #         else:
        #             print(f"ERROR: Variable {bool_operation[1][1]} does not exist or is not defined")
        #     else:
        #         x=bool_operation[1][1]

        #     if x=="WIN":
        #         x= 1
        #     else:
        #         x=0
        #     if bool_operation[3][0]== "variable":
        #         if bool_operation[3][1] in symbol_table:
        #             y= symbol_table[bool_operation[3][1]]
        #             if y!="WIN" and y!="FAIL":
        #                 print(f"ERROR: Invalid Variable")
        #                 exit()
        #         else:
        #             print(f"ERROR: Variable {bool_operation[3][1]} does not exist or is not defined")
        #     else:
        #         y=bool_operation[3][1]
        #     if y=="WIN":
        #         y=1
        #     else:
        #         y=0
        #     if x ^ y == 1:
        #         return (("TROOF","WIN"))
        #     else:
        #         return (("TROOF","FAIL"))
        # elif re.search(r"NOT", bool_operation[0][1]):
        #     if bool_operation[1][0]== "variable":
        #         if bool_operation[1][1] in symbol_table:
        #             x= symbol_table[bool_operation[1][1]]

        #             if x!="WIN" and x!="FAIL":
        #                 print(f"ERROR: Invalid Variable")
        #                 exit()
        #         else:
        #             print(f"ERROR: Variable {bool_operation[1][1]} does not exist or is not defined")
        #     else:
        #         x=bool_operation[1][1]

        #     if x=="WIN":
        #         x= 1
        #     else:
        #         x=0
        #     if not x==True:
        #         return (("TROOF","WIN"))
        #     else:
        #         return (("TROOF","FAIL"))
        # elif re.search(r"ALL OF",bool_operation[0][1]):
        #     if bool_operation[-1][1]!= "MKAY":
        #         print('ERROR: This operation requires a "MKAY" at the end')
        #         exit()
        #     bool_operation.pop(-1)
        #     result_bool= True
        
        #     # CHECKS ALL OPERANDS/ EXPRESSION AND CHECK IF THEY ARE TRUE OR NOT ; IF IT ENCOUNTERS A FALSE IMMEDIATELY RETURN
        #     for i in range(len(bool_operation)-1,-1,-1):
        #         #Find the last AN
                
        #         if re.search(r"NUMBAR",bool_operation[i][0]) or re.search(r"NUMBR",bool_operation[i][0]) or re.search(r"BOTH OF", bool_operation[i][1]) or re.search(r"EITHER OF", bool_operation[i][1]) or re.search(r"WON OF", bool_operation[i][1]) or re.search(r"WON OF", bool_operation[i][1]) or re.search(r"variable",bool_operation[i][0]) or (i==1 and bool_operation[i][0]=="variable"): # ALSO ADD the last condition since if the 2nd operand of the ANY OF is a variable it would not be detected
        #             #Call this function again
        #             if bool_operation[i][1]== "NOT":
        #                 temp = self.boolean_expression(bool_operation[i],bool_operation[i+1])
        #                 print(temp)
        #                 if temp[1] =="WIN":
        #                     bool_temp = True
        #                 else:
        #                     bool_temp=False
        #                 #Immediately return since if one is false in ALL OF then its false no matter the value of the operands
        #                 if result_bool and bool_temp == False:
        #                     return(("TROOF","FAIL"))
        #             elif bool_operation[i][0]=="variable":
        #                 #CHECK IF variable exists
        #                 if bool_operation[i][1] in symbol_table:
        #                     temp = symbol_table[bool_operation[i][1]]
                            
        #                     if temp =="WIN":
        #                         bool_temp = True
        #                     else:
        #                         bool_temp=False
        #                     if result_bool and bool_temp == False:
                                
        #                         return(("TROOF","FAIL"))
        #                 else:
        #                     print(f"ERROR: Variable {bool_operation[1][1]} does not exist or is not defined")
        #             elif bool_operation[i][0] == "NUMBAR" or bool_operation[i][0] == "NUMBR":
        #                 if bool_operation[i][1]>0:
        #                     bool_temp = True
        #                 else:
        #                     bool_temp =False
        #                 if result_bool and bool_temp == False:
        #                     return(("TROOF","FAIL"))
        #             else:
        #                 temp = self.boolean_expression([bool_operation[i],bool_operation[i+1],bool_operation[i+2],bool_operation[i+3]])
                       
        #                 if temp[1] =="WIN":
        #                     bool_temp = True
        #                 else:
        #                     bool_temp=False
        #                 if result_bool and bool_temp == False:
        #                     return(("TROOF","FAIL"))
                    
        #     return (("TROOF","WIN"))
        # elif re.search(r"ANY OF",bool_operation[0][1]):
        
        #     if bool_operation[-1][1]!= "MKAY":
        #         print('ERROR: This operation requires a "MKAY" at the end')
        #         exit()
        #     bool_operation.pop(-1)
        #     result_bool= False
        #     # CHECKS ALL OPERANDS/ EXPRESSION AND CHECK IF THEY ARE TRUE OR NOT ; IF IT ENCOUNTERS A FALSE IMMEDIATELY RETURN
        #     for i in range(len(bool_operation)-2,-1,-1):
        #         #Find the last AN
        #         if re.search(r"BOTH OF", bool_operation[i][1]) or re.search(r"EITHER OF", bool_operation[i][1]) or re.search(r"WON OF", bool_operation[i][1]) or re.search(r"WON OF", bool_operation[i][1]) or re.search(r"variable",bool_operation[i][0]) or (i==1 and bool_operation[i][0]=="variable"):
                       
                    
        #             #Call this function again
        #             if bool_operation[i][1]== "NOT":
        #                 temp = self.boolean_expression(bool_operation[i],bool_operation[i+1])
    
        #                 if temp[1] =="WIN":
        #                     bool_temp = True
        #                 else:
        #                     bool_temp=False
        #                 #Immediately return since if one is false in ALL OF then its false no matter the value of the operands
        #                 if result_bool or bool_temp == True:
        #                     return(("TROOF","WIN"))
        #             elif bool_operation[i][0]=="variable":
        #                 #CHECK IF variable exists
        #                 if bool_operation[i][1] in symbol_table:
        #                     temp = symbol_table[bool_operation[i][1]]
        #                     if temp[1] =="WIN":
        #                         bool_temp = True
        #                     else:
        #                         bool_temp=False
        #                     if result_bool and bool_temp == False:
        #                         return(("TROOF","FAIL"))
        #                 else:
        #                     print(f"ERROR: Variable {bool_operation[1][1]} does not exist or is not defined")
        #             else:
        #                 temp = self.boolean_expression([bool_operation[i],bool_operation[i+1],bool_operation[i+2],bool_operation[i+3]])
                    
        #                 if temp[1] =="WIN":
        #                     bool_temp = True
        #                 else:
        #                     bool_temp=False
        #                 if result_bool or bool_temp == True:
        #                     return(("TROOF","WIN"))
                    
        #     return (("TROOF","FAIL"))

    #RETURN TYPE TUPLE OF TROOF, WIN|FAIL
    def comparison(self,comp_exp):
        if (comp_exp[1][0]=="variable" and (comp_exp[3][1]== "BIGGR OF" or comp_exp[3][1]== "SMALLR OF")) or (((comp_exp[1][1]== "BIGGR OF" or comp_exp[1][1]== "SMALLR OF")) and comp_exp[2]== comp_exp[6]): #case for 
            print("Test")
          
            if comp_exp[3][1]== "BIGGR OF" or comp_exp[3][1]== "SMALLR OF": # case for x AN BIGGR OF X AN Yformat
                
                if comp_exp[0][1]=="BOTH SAEM":
                    if comp_exp[1][0]=="variable":
                        if comp_exp[1][1] in symbol_table:
                            x= symbol_table[comp_exp[1][1]] #assign that to x
                            if x=="WIN":
                                x=1
                            elif x == "FAIL":
                                x=0
                        else:
                            print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
                            exit()
                        
                    else:
                        x=comp_exp[1][1]
                    if comp_exp[6][0]=="variable":
                        if comp_exp[6][1] in symbol_table:
                            y= symbol_table[comp_exp[6][1]]
                            if y== "WIN":
                                y=1
                            elif x == "FAIL":
                                y=0
                        else:
                            print(f"ERROR: Variable {comp_exp[6][1]} does not exist or is not defined")
                            exit()
                    else:
                        y=comp_exp[6][1]
                    if isinstance(x,str) and (isinstance(y,int) or isinstance(y,float)):
                        if isinstance(y,int) and x.isdigit():

                            x= int(x)
                        else:
                            x=float(x)
                    if isinstance(y,str) and (isinstance(x,int) or isinstance(x,float)):
                        if isinstance(x,int) and y.isdigit():
                            y=int(y)
                        else:
                            y=float(y)
                    if comp_exp[3][1]=="BIGGR OF":
                        if x>=y:
                            return(("TROOF","WIN"))
                        else:
                            return(("TROOF","FAIL"))
                    else:#CASE FOR SMALLR OF
                        if x<=y:
                            return(("TROOF","WIN"))
                        else:
                            return(("TROOF","FAIL"))
                #DIFFRINT
                elif comp_exp[0][1] == "DIFFRINT":
                
                    if comp_exp[1][0]=="variable":
                        if comp_exp[1][1] in symbol_table:
                            x= symbol_table[comp_exp[1][1]] #assign that to x
                            if x=="WIN":
                                x=1
                            elif x == "FAIL":
                                x=0
                        else:
                            print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
                            exit()

                    else:
                        x=comp_exp[1][1]
                    if comp_exp[6][0]=="variable":
                        if comp_exp[6][1] in symbol_table:
                            y= symbol_table[comp_exp[6][1]]
                            if y== "WIN":
                                y=1
                            elif x == "FAIL":
                                y=0
                        else:
                            print(f"ERROR: Variable {comp_exp[6][1]} does not exist or is not defined")
                            exit()
                    else:
                        y=comp_exp[6][1]
                    if isinstance(x,str) and (isinstance(y,int) or isinstance(y,float)):
                        if isinstance(y,int) and x.isdigit():

                            x= int(x)
                        else:
                            x=float(x)
                    if isinstance(y,str) and (isinstance(x,int) or isinstance(x,float)):
                        if isinstance(x,int) and y.isdigit():
                            y=int(y)
                        else:
                            y=float(y)
                    if comp_exp[3][1]=="BIGGR OF":
                        if x>y:
                            return(("TROOF","WIN"))
                        else:
                            return(("TROOF","FAIL"))
                    else:#CASE FOR SMALLR OF
                        if x<y:
                            return(("TROOF","WIN"))
                        else:
                            return(("TROOF","FAIL"))
            else:   #Case for format <comparison_operator> BIGGR OF | SMALLR OF x AN y an x
                if comp_exp[0][1]=="BOTH SAEM":
                    if comp_exp[2][0]=="variable":
                        if comp_exp[2][1] in symbol_table:
                            x= symbol_table[comp_exp[2][1]] #assign that to x
                            if x=="WIN":
                                x=1
                            elif x == "FAIL":
                                x=0
                        else:
                            print(f"ERROR: Variable {comp_exp[2][1]} does not exist or is not defined")
                            exit()
                        
                    else:
                        x=comp_exp[2][1]
                    if comp_exp[4][0]=="variable":
                        if comp_exp[4][1] in symbol_table:
                            y= symbol_table[comp_exp[4][1]]
                            if y== "WIN":
                                y=1
                            elif x == "FAIL":
                                y=0
                        else:
                            print(f"ERROR: Variable {comp_exp[4][1]} does not exist or is not defined")
                            exit()
                    else:
                        y=comp_exp[4][1]
                    if isinstance(x,str) and (isinstance(y,int) or isinstance(y,float)):
                        if isinstance(y,int) and x.isdigit():

                            x= int(x)
                        else:
                            x=float(x)
                    if isinstance(y,str) and (isinstance(x,int) or isinstance(x,float)):
                        if isinstance(x,int) and y.isdigit():
                            y=int(y)
                        else:
                            y=float(y)
                    if comp_exp[1][1]=="BIGGR OF":
                        if x>=y:
                        
                            return(("TROOF","WIN"))
                        else:
                            
                            return(("TROOF","FAIL"))
                    else:#CASE FOR SMALLR OF
                        if x<=y:
                            return(("TROOF","WIN"))
                        else:
                            return(("TROOF","FAIL"))
                elif comp_exp[0][1]=="DIFFRINT":
                    if comp_exp[2][0]=="variable":
                        if comp_exp[2][1] in symbol_table:
                            x= symbol_table[comp_exp[2][1]] #assign that to x
                            if x=="WIN":
                                x=1
                            elif x == "FAIL":
                                x=0
                        else:
                            print(f"ERROR: Variable {comp_exp[2][1]} does not exist or is not defined")
                            exit()
                        
                    else:
                        x=comp_exp[2][1]
                    if comp_exp[4][0]=="variable":
                        if comp_exp[4][1] in symbol_table:
                            y= symbol_table[comp_exp[4][1]]
                            if y== "WIN":
                                y=1
                            elif y == "FAIL":
                                y=0
                        else:
                            print(f"ERROR: Variable {comp_exp[4][1]} does not exist or is not defined")
                            exit()
                    else:
                        y=comp_exp[4][1]
                    if isinstance(x,str) and (isinstance(y,int) or isinstance(y,float)):
                        if isinstance(y,int) and x.isdigit():

                            x= int(x)
                        else:
                            x=float(x)
                    if isinstance(y,str) and (isinstance(x,int) or isinstance(x,float)):
                        if isinstance(x,int) and y.isdigit():
                            y=int(y)
                        else:
                            y=float(y)
                    if comp_exp[1][1]=="BIGGR OF":
                        if x>y:
                            return(("TROOF","WIN"))
                        else:
                            return(("TROOF","FAIL"))
                    else:#CASE FOR SMALLR OF
                        if x<y:
                            return(("TROOF","WIN"))
                        else:
                            return(("TROOF","FAIL"))
                

        else: #CASE FOR COMPARISON OPERATOR
            if comp_exp[0][1]=="BOTH SAEM":
                if comp_exp[1][0]=="variable":
                    if comp_exp[1][1] in symbol_table:
                        x= symbol_table[comp_exp[1][1]] #assign that to x
                        if x=="WIN":
                            x=1
                        elif x == "FAIL":
                            x=0
                    else:
                        print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
                        exit()
                        
                else:
                    x=comp_exp[1][1]
                if comp_exp[3][0]=="variable":
                    if comp_exp[3][1] in symbol_table:
                        y= symbol_table[comp_exp[3][1]]
                        if y== "WIN":
                            y=1
                        elif y == "FAIL":
                            y=0
                    else:
                        print(f"ERROR: Variable {comp_exp[3][1]} does not exist or is not defined")
                        exit()
                else:
                    y=comp_exp[3][1]
                if isinstance(x,str) and (isinstance(y,int) or isinstance(y,float)):
                    if isinstance(y,int) and x.isdigit():
                        
                        x= int(x)
                    else:
                        x=float(x)
                if isinstance(y,str) and (isinstance(x,int) or isinstance(x,float)):
                    if isinstance(x,int) and y.isdigit():
                        y=int(y)
                    else:
                        y=float(y)
                
                if x==y:
                    return(("TROOF","WIN"))
                else:
                    return(("TROOF","FAIL"))
            elif comp_exp[0][1]=="DIFFRINT":
                if comp_exp[1][0]=="variable":
                    if comp_exp[1][1] in symbol_table:
                        x= symbol_table[comp_exp[1][1]] #assign that to x
                        if x=="WIN":
                            x=1
                        elif x == "FAIL":
                            x=0
                    else:
                        print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
                        exit()
                        
                else:
                    x=comp_exp[1][1]
                if comp_exp[3][0]=="variable":
                    if comp_exp[3][1] in symbol_table:
                        y= symbol_table[comp_exp[3][1]]
                        if y== "WIN":
                            y=1
                        elif y == "FAIL":
                            y=0
                    else:
                        print(f"ERROR: Variable {comp_exp[3][1]} does not exist or is not defined")
                        exit()
                else:
                    y=comp_exp[3][1]
                if isinstance(x,str) and (isinstance(y,int) or isinstance(y,float)):
                    if isinstance(y,int) and x.isdigit():
                        
                        x= int(x)
                    else:
                        x=float(x)
                if isinstance(y,str) and (isinstance(x,int) or isinstance(x,float)):
                    if isinstance(x,int) and y.isdigit():
                        y=int(y)
                    else:
                        y=float(y)
                
                if x!=y:
                    return(("TROOF","WIN"))
                else:
                    return(("TROOF","FAIL"))
        # if re.search(r"BOTH SAEM",comp_exp[0][1]):     
        #     if isinstance(comp_exp[3][1],str) and re.search(r"BIGGR OF", comp_exp[3][1]):
        #         print("POTA")
        #         if comp_exp[1] != comp_exp[4]:
        #             print("SYNTAX ERROR")
        #             exit() #Replace something that can halt the main program
        #         else:
        #             if comp_exp[1][0]=="variable":
        #                 if comp_exp[1][1] in symbol_table:
        #                     x= symbol_table[comp_exp[1][1]] #assign that to x

        #                 else:
        #                     print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
        #                     exit()

        #             else:
        #                 x=comp_exp[1][1]
        #             if comp_exp[6][0]=="variable":
        #                 if comp_exp[6][1] in symbol_table:
        #                     y= symbol_table[comp_exp[6][1]]
                            

        #                 else:
        #                     print(f"ERROR: Variable {comp_exp[6][1]} does not exist or is not defined")
        #                     exit()
        #             else:
        #                 y=comp_exp[6][1]
        #             print(f"x{x}y{y}")
        #             if x>=y:
        #                 return ("TROOF", "WIN")
        #             else:
        #                 return ("TROOF", "FAIL")
                    
        #     elif isinstance(comp_exp[3][1],str) and re.search(r"SMALLR OF", comp_exp[3][1]):
               
        #         if comp_exp[1]!= comp_exp[4]:
        #             print("SYNTAX ERROR")
        #             exit() #Replace something that can halt the main program
        #         else:
        #             if comp_exp[1][0]=="variable":
        #                 if comp_exp[1][1] in symbol_table:
        #                     x= symbol_table[comp_exp[1][1]]

        #                 else:
        #                     print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
        #                     exit()

        #             else:
        #                 x=comp_exp[1][1]
        
        #             if comp_exp[6][0]=="variable":
        #                 if comp_exp[6][1] in symbol_table:
        #                     y= symbol_table[comp_exp[6][1]]
        #                 else:
        #                     print(f"ERROR: Variable {comp_exp[6][1]} does not exist or is not defined")
        #                     exit()
        #             else:
        #                 y=comp_exp[6][1]
        #             if x<=y:
        #                 return ("TROOF", "WIN")
        #             else:
        #                 return ("TROOF", "FAIL")
        #     else:
        #         if comp_exp[1][0]=="variable":
        #             if comp_exp[1][1] in symbol_table:
        #                 x= symbol_table[comp_exp[1][1]]

        #             else:
        #                 print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
        #                 exit()

        #         else:
        #             x=comp_exp[1][1]
        #         if comp_exp[3][0]=="variable":
        #             if comp_exp[3][1] in symbol_table:
        #                 y= symbol_table[comp_exp[3][1]]
                        

        #             else:
        #                 print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
        #         else:
        #             y=comp_exp[3][1]
        #         if x==y:
        #             return ("TROOF", "WIN")
        #         else:
        #             return ("TROOF", "FAIL")
        # elif re.search(r"DIFFRINT", comp_exp[0][1]):
            
            
        #     if isinstance(comp_exp[3][1],str) and re.search(r"BIGGR OF", comp_exp[3][1]):
        #         print("Hey")
        #         if comp_exp[1] != comp_exp[4]:
        #             print("SYNTAX ERROR")
        #             exit() #Replace something that can halt the main program
        #         else:
        #             if comp_exp[1][0]=="variable":
        #                 if comp_exp[1][1] in symbol_table:
        #                     x= symbol_table[comp_exp[1][1]]

        #                 else:
        #                     print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
        #                     exit()

        #             else:
        #                 x=comp_exp[1][1]
        #             if comp_exp[6][0]=="variable":
        #                 if comp_exp[6][1] in symbol_table:
        #                     y= symbol_table[comp_exp[6][1]]
        #                 else:
        #                     print(f"ERROR: Variable {comp_exp[6][1]} does not exist or is not defined")
        #                     exit()
        #             else:
        #                 y=comp_exp[6][1]
                    
        #             if x>y:
        #                 return ("TROOF", "WIN")
        #             else:
        #                 return ("TROOF", "FAIL")
                    
        #     elif isinstance(comp_exp[3][1],str) and  re.search(r"SMALLR OF", comp_exp[3][1]):
        #         if comp_exp[1] != comp_exp[4]:
        #             print("SYNTAX ERROR")
        #             exit() #Replace something that can halt the main program
        #         else:
        #             if comp_exp[1][0]=="variable":
        #                 if comp_exp[1][1] in symbol_table:
        #                     x= symbol_table[comp_exp[1][1]]

        #                 else:
        #                     print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
        #                     exit()

        #             else:
        #                 x=comp_exp[1][1]
        
        #             if comp_exp[6][0]=="variable":
        #                 if comp_exp[6][1] in symbol_table:
        #                     y= symbol_table[comp_exp[6][1]]
        #                 else:
        #                     print(f"ERROR: Variable {comp_exp[6][1]} does not exist or is not defined")
        #                     exit()
        #             else:
        #                 y=comp_exp[6][1]
        #             if x<y:
        #                 return ("TROOF", "WIN")
        #             else:
        #                 return ("TROOF", "FAIL")
        #     else:
                
        #         if comp_exp[1][0]=="variable":
        #             if comp_exp[1][1] in symbol_table:
        #                 x= symbol_table[comp_exp[1][1]]
        #             else:
        #                 print(f"ERROR: Variable {comp_exp[1][1]} does not exist or is not defined")
        #                 exit()
        #         else:
        #             x=comp_exp[1][1]
        #         if comp_exp[3][0]=="variable":
        #             if comp_exp[3][1] in symbol_table:
        #                 y= symbol_table[comp_exp[3][1]]

        #             else:
        #                 print(f"ERROR: Variable {comp_exp[3][1]} does not exist or is not defined")
        #         else:
        #             y=comp_exp[3][1]
        #         if x!=y:
        #             return ("TROOF", "WIN")
        #         else:
        #             return ("TROOF", "FAIL")
               
                
    def arithmetic_expression(self,ar_operation):
        for i in range(len(ar_operation)-1,-1, -1):
                    
            if not re.search(r"NUMBR",ar_operation[i][0]) and not re.search(r"NUMBAR",ar_operation[i][0])  and re.search(r"SUM OF", ar_operation[i][1]):

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
                            if x=="FAIL":
                                x= 0
                            elif x=="WIN":
                                x=1
                            elif x.isdigit():
                                x= int(x) 
                            else: # Do another check if its float since digit only checks if int
                                try:
                                    x= float(x)
                                except ValueError:
                                    print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR or can be typecasted to those said types")
                                    exit()
                                
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index-1][1]}does not exists")
                else:
                    if isinstance(ar_operation[temp_index-1][1],str):
                        x = ar_operation[temp_index-1][1]
                        if x=="FAIL":
                            x= 0
                        elif x=="WIN":
                            x=1
                        elif x.isdigit():
                            x= int(x) 
                        else: # Do another check if its float since digit only checks if int
                            try:
                                x= float(x)
                            except ValueError:
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR or can be typecasted to those said types")
                                exit()
                    else:
                        x = ar_operation[temp_index-1][1]
                if ar_operation[temp_index+1][0] == "variable":
                    if ar_operation[temp_index+1][1] in symbol_table:
                        y= symbol_table[ar_operation[temp_index+1][1]]
                        if not isinstance(y,float) and not isinstance(y,int):
                            if y=="FAIL":
                                y= 0
                            elif y=="WIN":
                                y=1
                            elif y.isdigit():
                                y= int(y)
                        
                            else:
                                try:
                                    y= float(y)
                                except ValueError:
                                    print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                    exit()
                    
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index+1][1]}does not exists")
                else:
                    if isinstance(ar_operation[temp_index+1][1],str):
                        y = ar_operation[temp_index+1][1]
                        if y=="FAIL":
                                y= 0
                        elif y=="WIN":
                            y=1
                        elif y.isdigit():
                            y= int(y)
                    
                        else:
                            try:
                                y= float(y)
                            except ValueError:
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                exit()
                    else:
                        y = ar_operation[temp_index+1][1]
                print(f"X:{x} and Y:{y}")
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
                            if x=="FAIL":
                                x= 0
                            elif x=="WIN":
                                x=1
                            elif x.isdigit():
                                x= int(x) 
                            else: # Do another check if its float since digit only checks if int
                                try:
                                    x= float(x)
                                except ValueError:
                                    print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR or can be typecasted to those said types")
                                    exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index-1][1]}does not exists")
                else:
                    if isinstance(ar_operation[temp_index-1][1],str):
                        x = ar_operation[temp_index-1][1]
                        if x=="FAIL":
                            x= 0
                        elif x=="WIN":
                            x=1
                        elif x.isdigit():
                            x= int(x) 
                        else: # Do another check if its float since digit only checks if int
                            try:
                                x= float(x)
                            except ValueError:
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR or can be typecasted to those said types")
                                exit()
                    else:
                        x = ar_operation[temp_index-1][1]
                if ar_operation[temp_index+1][0] == "variable":
                    if ar_operation[temp_index+1][1] in symbol_table:
                        y= symbol_table[ar_operation[temp_index+1][1]]
                        if not isinstance(y,float) and not isinstance(y,int):
                            if y=="FAIL":
                                y= 0
                            elif y=="WIN":
                                y=1
                            elif y.isdigit():
                                y= int(y)
                        
                            else:
                                try:
                                    y= float(y)
                                except ValueError:
                                    print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                    exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index+1][1]}does not exists")
                else:
                    if isinstance(ar_operation[temp_index+1][1],str):
                        y = ar_operation[temp_index+1][1]
                        if y=="FAIL":
                                y= 0
                        elif y=="WIN":
                            y=1
                        elif y.isdigit():
                            y= int(y)
                    
                        else:
                            try:
                                y= float(y)
                            except ValueError:
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                exit()
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
                            if x=="FAIL":
                                x= 0
                            elif x=="WIN":
                                x=1
                            elif x.isdigit():
                                x= int(x) 
                            else: # Do another check if its float since digit only checks if int
                                try:
                                    x= float(x)
                                except ValueError:
                                    print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR or can be typecasted to those said types")
                                    exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index-1][1]}does not exists")
                else:
                    if isinstance(ar_operation[temp_index-1][1],str):
                        x = ar_operation[temp_index-1][1]
                        if x=="FAIL":
                            x= 0
                        elif x=="WIN":
                            x=1
                        elif x.isdigit():
                            x= int(x) 
                        else: # Do another check if its float since digit only checks if int
                            try:
                                x= float(x)
                            except ValueError:
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR or can be typecasted to those said types")
                                exit()
                    else:
                        x = ar_operation[temp_index-1][1]
                if ar_operation[temp_index+1][0] == "variable":
                    if ar_operation[temp_index+1][1] in symbol_table:
                        y= symbol_table[ar_operation[temp_index+1][1]]
                        if not isinstance(y,float) and not isinstance(y,int):
                            if y=="FAIL":
                                y= 0
                            elif y=="WIN":
                                y=1
                            elif y.isdigit():
                                y= int(y)
                        
                            else:
                                try:
                                    y= float(y)
                                except ValueError:
                                    print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                    exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index+1][1]}does not exists")
                else:
                    if isinstance(ar_operation[temp_index+1][1],str):
                        y = ar_operation[temp_index+1][1]
                        if y=="FAIL":
                                y= 0
                        elif y=="WIN":
                            y=1
                        elif y.isdigit():
                            y= int(y)
                    
                        else:
                            try:
                                y= float(y)
                            except ValueError:
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                exit()
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
                            if x=="FAIL":
                                x= 0
                            elif x=="WIN":
                                x=1
                            elif x.isdigit():
                                x= int(x) 
                            else: # Do another check if its float since digit only checks if int
                                try:
                                    x= float(x)
                                except ValueError:
                                    print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR or can be typecasted to those said types")
                                    exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index-1][1]}does not exists")
                else:
                    if isinstance(ar_operation[temp_index-1][1],str):
                        
                        x = ar_operation[temp_index-1][1].strip('"')
                        
                        if x=="FAIL":
                            x= 0
                        elif x=="WIN":
                            x=1
                        elif x.isdigit():
                            
                            x= int(x) 
                        else: # Do another check if its float since digit only checks if int
                            try:
                                x= float(x)
                            except ValueError:
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR or can be typecasted to those said types")
                                exit()
                    else:
                        x = ar_operation[temp_index-1][1]
                if ar_operation[temp_index+1][0] == "variable":
                    if ar_operation[temp_index+1][1] in symbol_table:
                        y= symbol_table[ar_operation[temp_index+1][1]]
                        if not isinstance(y,float) and not isinstance(y,int):
                            if y=="FAIL":
                                y= 0
                            elif y=="WIN":
                                y=1
                            elif y.isdigit():
                                y= int(y)
                        
                            else:
                                try:
                                    y= float(y)
                                except ValueError:
                                    print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                    exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index+1][1]}does not exists")
                else:
                    if isinstance(ar_operation[temp_index+1][1],str):
                        y = ar_operation[temp_index+1][1]
                        if y=="FAIL":
                                y= 0
                        elif y=="WIN":
                            y=1
                        elif y.isdigit():
                            y= int(y)
                    
                        else:
                            try:
                                y= float(y)
                            except ValueError:
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                exit()
                    else:
                        y = ar_operation[temp_index+1][1]
                temp_val= x/y
                if isinstance(x,int) and isinstance(y,int): #Quoshunt is the only case where both operand is type NUMBR and can result to a float or NUMBAR so if both is NUMBR typecast it into NUMBR
                    
                    temp_val = ("NUMBR", int(temp_val))
                else:
                    temp_val = ("NUMBAR",temp_val)
                ar_operation.insert(i,temp_val)
                #pop the sum of, left operand , "AN" , and ,right operand
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
                ar_operation.pop(i+1)
            #FOR MAX AND MIN IMPLEMENTATION
            elif  not re.search(r"NUMBR",ar_operation[i][0]) and not re.search(r"NUMBAR",ar_operation[i][0]) and re.search(r"BIGGR OF",ar_operation[i][1]):
                    temp_index=i
                    while 1:
                        if  not re.search(r"NUMBR",ar_operation[temp_index][0]) and not re.search(r"NUMBAR",ar_operation[temp_index][0]) and re.search(r"AN", ar_operation[temp_index][1]):
                            break
                        temp_index+=1
                    
                    #Evaluate X ; Check if variable or not
                    if ar_operation[temp_index-1][0] == "variable":
                        if ar_operation[temp_index-1][1] in symbol_table:
                            x= symbol_table[ar_operation[temp_index-1][1]]
                            if not isinstance(x,float) and not isinstance(x,int):
                                if x=="FAIL":
                                    x= 0
                                elif x=="WIN":
                                    x=1
                                elif x.isdigit():
                                    x= int(x) 
                                else: # Do another check if its float since digit only checks if int
                                    try:
                                        x= float(x)
                                    except ValueError:
                                        print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR or can be typecasted to those said types")
                                        exit()
                        else:
                            print(f"ERROR: Variable {ar_operation[temp_index-1][1]}does not exists")
                    else:
                        if isinstance(ar_operation[temp_index-1][1],str):
                            x = ar_operation[temp_index-1][1]
                            if x=="FAIL":
                                x= 0
                            elif x=="WIN":
                                x=1
                            elif x.isdigit():
                                x= int(x) 
                            else: # Do another check if its float since digit only checks if int
                                try:
                                    x= float(x)
                                except ValueError:
                                    print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR or can be typecasted to those said types")
                                    exit()
                        else:
                            x = ar_operation[temp_index-1][1]
                    #Evaluate Y
                    if ar_operation[temp_index+1][0] == "variable":
                        if ar_operation[temp_index+1][1] in symbol_table:
                            y= symbol_table[ar_operation[temp_index+1][1]]
                            if not isinstance(y,float) and not isinstance(y,int):
                                if y=="FAIL":
                                    y= 0
                                elif y=="WIN":
                                    y=1
                                elif y.isdigit():
                                    y= int(y)
                                else:
                                    try:
                                        y= float(y)
                                    except ValueError:
                                        print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                        exit()
                        else:
                            print(f"ERROR: Variable {ar_operation[temp_index+1][1]}does not exists")
                    else:
                        if isinstance(ar_operation[temp_index+1][1],str):
                            y = ar_operation[temp_index+1][1]
                            if y=="FAIL":
                                    y= 0
                            elif y=="WIN":
                                y=1
                            elif y.isdigit():
                                y= int(y)
                        
                            else:
                                try:
                                    y= float(y)
                                except ValueError:
                                    print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                    exit()
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
                #For max() method
                
                #Minimum
            elif not re.search(r"NUMBR",ar_operation[i][0]) and not re.search(r"NUMBAR",ar_operation[i][0]) and re.search(r"SMALLR OF",ar_operation[i][1]):
                temp_index=i

                while 1:
                    if  not re.search(r"NUMBR",ar_operation[temp_index][0]) and not re.search(r"NUMBAR",ar_operation[temp_index][0]) and re.search(r"AN", ar_operation[temp_index][1]):
                        break
                    temp_index+=1
                
                #Evaluate X ; Check if variable or not
                if ar_operation[temp_index-1][0] == "variable":
                    if ar_operation[temp_index-1][1] in symbol_table:
                        x= symbol_table[ar_operation[temp_index-1][1]]
                        if not isinstance(x,float) and not isinstance(x,int):
                            if x=="FAIL":
                                    x= 0
                            elif x=="WIN":
                                x=1
                            elif x.isdigit():
                                x= int(x) 
                            else: # Do another check if its float since digit only checks if int
                                try:
                                    x= float(x)
                                except ValueError:
                                    print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR or can be typecasted to those said types")
                                    exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index-1][1]}does not exists")
                else:
                    if isinstance(ar_operation[temp_index-1][1],str):
                        x = ar_operation[temp_index-1][1]
                        if x=="FAIL":
                            x= 0
                        elif x=="WIN":
                            x=1
                        elif x.isdigit():
                            x= int(x) 
                        else: # Do another check if its float since digit only checks if int
                            try:
                                x= float(x)
                            except ValueError:
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR or can be typecasted to those said types")
                                exit()
                    else:
                        x = ar_operation[temp_index-1][1]
                #Evaluate Y
                if ar_operation[temp_index+1][0] == "variable":
                    if ar_operation[temp_index+1][1] in symbol_table:
                        y= symbol_table[ar_operation[temp_index+1][1]]
                        if not isinstance(y,float) and not isinstance(y,int):
                            if y=="FAIL":
                                    y= 0
                            elif y=="WIN":
                                y=1
                            elif y.isdigit():
                                y= int(y)
                            else:
                                try:
                                    y= float(y)
                                except ValueError:
                                    print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                    exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index+1][1]}does not exists")
                else:
                    if isinstance(ar_operation[temp_index+1][1],str):
                        y = ar_operation[temp_index+1][1]
                        if y=="FAIL":
                                y= 0
                        elif y=="WIN":
                            y=1
                        elif y.isdigit():
                            y= int(y)
                    
                        else:
                            try:
                                y= float(y)
                            except ValueError:
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                exit()
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
            elif  not re.search(r"NUMBR",ar_operation[i][0]) and not re.search(r"NUMBAR",ar_operation[i][0]) and re.search(r"MOD OF",ar_operation[i][1]):
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
                            if x=="FAIL":
                                    x= 0
                            elif x=="WIN":
                                x=1
                            elif x.isdigit():
                                x= int(x) 
                            else: # Do another check if its float since digit only checks if int
                                try:
                                    x= float(x)
                                except ValueError:
                                    print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR or can be typecasted to those said types")
                                    exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index-1][1]}does not exists")
                else:
                    if isinstance(ar_operation[temp_index-1][1],str):
                        x = ar_operation[temp_index-1][1]
                        if x=="FAIL":
                            x= 0
                        elif x=="WIN":
                            x=1
                        elif x.isdigit():
                            x= int(x) 
                        else: # Do another check if its float since digit only checks if int
                            try:
                                x= float(x)
                            except ValueError:
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR or can be typecasted to those said types")
                                exit()
                    else:
                        x = ar_operation[temp_index-1][1]
                if ar_operation[temp_index+1][0] == "variable":
                    if ar_operation[temp_index+1][1] in symbol_table:
                        y= symbol_table[ar_operation[temp_index+1][1]]
                        if not isinstance(y,float) and not isinstance(y,int):
                            if y=="FAIL":
                                    y= 0
                            elif y=="WIN":
                                y=1
                            elif y.isdigit():
                                y= int(y)
                            else:
                                try:
                                    y= float(y)
                                except ValueError:
                                    print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                    exit()
                    else:
                        print(f"ERROR: Variable {ar_operation[temp_index+1][1]}does not exists")
                else:
                    if isinstance(ar_operation[temp_index+1][1],str):
                        y = ar_operation[temp_index+1][1]
                        if y=="FAIL":
                                y= 0
                        elif y=="WIN":
                            y=1
                        elif y.isdigit():
                            y= int(y)
                    
                        else:
                            try:
                                y= float(y)
                            except ValueError:
                                print(f"ERROR: Invalid Data type {ar_operation[temp_index-1][1]} must be of data type NUMBR or NUMBAR")
                                exit()
                    else:
                        y = ar_operation[temp_index+1][1]
                temp_val= x%y
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
        return ar_operation[0][1]
    def check_varname(self,varname):
        pattern= r"[A-Za-z][A-Za-z\d]*"
        if re.search(pattern, varname):
            return True
        else:
            return False
    def parse_expression(self):
        global declaration_status
        global ifelse_flag
        if ifelse_flag==1:
            if re.search(visible, self.tokens[0][1]):
        
                self.tokens.pop(0)
                temp=self.tokens.copy()
                temp_operands= []
                symbol_table["IT"]="" # reset IT
                # find each visible_concat
                i=0
                loop_flag=0
                while i<len(self.tokens): # THIS LOOP SEPERATES EACH OPERAND TO BE CONCATENATED
                    
                    index_concat= i

                    while True:
                        if index_concat>=len(self.tokens): # LAST Indexed has reached its either its the last operand after a + or there is no +to begin with
                            
                            loop_back=len(self.tokens)-1
                            #Loop to go back to the last + or the first index
                            while loop_back!=0:
                                if self.tokens[loop_back][0]=="visible_concat":
                                    break
                                loop_back-=1
                            
                            if loop_back!=0: #Case for last +
                                temp_operands.append(self.tokens[loop_back+1:len(self.tokens)])
                            else: #Case there is no concatenation/ First index
                                temp_operands.append(self.tokens[0:len(self.tokens)])

                            break
                        elif self.tokens[index_concat][0]=="visible_concat":
                            
                            temp_operands.append(self.tokens[i:index_concat])
                            break
                        index_concat+=1
                    if loop_flag==1: #breaks out of this loop
                        break
                
                    i=index_concat+1
                
                for operand in temp_operands: # Iterate trough each operand
                    
                    
                    if operand[0][0]=="STRING":
                        
                        symbol_table["IT"]= symbol_table["IT"]+operand[0][1].strip('"')
                    elif re.search(r"arithmetic_operator", operand[0][0]):
                        
                        symbol_table["IT"]= symbol_table["IT"]+str(self.arithmetic_expression(operand))
                    elif re.search(r"variable", operand[0][0]):
                        if  operand[0][1] in symbol_table:
                            if isinstance(symbol_table[operand[0][1]],str):
                                symbol_table["IT"]= symbol_table["IT"]+symbol_table[operand[0][1]]
                            else:
                                symbol_table["IT"]= symbol_table["IT"]+str(symbol_table[operand[0][1]])
                        else:
                            print(f"ERROR: Variable {operand[0][1]} does not exist or is not defined")
                    elif re.search(r"concatenation", operand[0][0]):
                        
                        temp=operand.copy()
                
                        
                        val = self.concat(temp)
                        symbol_table["IT"] = symbol_table["IT"]+ str(val[1])                       
                    elif re.search(r"comparison_operator",operand[0][0]):
                        temp= operand.copy()
                        
                        #Do the evaluation by operand here due to how the function was made
                        val= self.comparison(temp)
                        
                        symbol_table["IT"] =symbol_table["IT"]+str(val[1])
                    elif re.search(r"boolean_operator", operand[0][0]):
                        temp= operand.copy()
                        val= self.boolean_expression(temp)
                        symbol_table["IT"] =symbol_table["IT"]+str(val[1])
                    elif re.search(r"TROOF", operand[0][0]):
                        symbol_table["IT"] =symbol_table["IT"]+str(operand[0][1])
                    elif re.search(r"NUMBR", operand[0][0]) or re.search(r"NUMBAR",operand[0][0]):
                        symbol_table["IT"]= symbol_table["IT"]+str(operand[0][1])
                    
            elif re.search(r"declaration_start", self.tokens[0][0]):
                declaration_status+=1
                
            elif re.search(r"declaration_end",self.tokens[0][0]):
                declaration_status+=1
            #DECLARATION
            elif re.search(r"declaration_keyword",self.tokens[0][0]):
                if declaration_status>1:
                    print("ERROR: Declare this variable inside the  WAZZUP-BUHBYE section")
                    exit()
                else:
                    if len(self.tokens)==2:
                        #Check if valid variable name
                        if self.check_varname(self.tokens[1][1]):  #INITIALIZATION 
                            symbol_table[self.tokens[1][1]]= "NOOB"
                        else:
                            print("ERROR: Invalid Variable name")
                            exit()
                    else:
                        if self.check_varname(self.tokens[1][1]):
                            temp1= self.tokens.copy() #Copy the token
                            temp1.pop(0) #Pop the I HAS A
                            varname = temp1.pop(0) #Put it into a temp variable and pop the varname
                            temp1.pop(0) # Pop ITZ 
                            #Evaluate the expression
                            if re.search(r"STRING",temp1[0][0]):
                                
                                symbol_table[varname[1]]=temp1[0][1].strip('"')
                            elif re.search(r"TROOF",temp1[0][0]):
                                
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
                                
                                symbol_table[varname[1]]=self.arithmetic_expression(temp)
                            
                            elif re.search(r"comparison_operator",temp1[0][0]):
                                temp= temp1.copy()
                                
                                val= self.comparison(temp)
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
            elif re.search(r"variable",self.tokens[0][0]) and re.search((r"reassignment_delimeter"),self.tokens[1][0]):
                if len(self.tokens)>2:
                    if self.tokens[0][1] in symbol_table:
                        temp1= self.tokens.copy() #Copy the token
            
                        varname = temp1.pop(0) #Put it into a temp variable and pop the varname
                        if temp1[0][1]=="R":
                            temp1.pop(0) # Pop R
                            #Evaluate the expressio
                            if re.search(r"STRING",temp1[0][0]):
                                
                                symbol_table[varname[1]]=temp1[0][1].strip('"')
                            elif re.search(r"TROOF",temp1[0][0]):
                                symbol_table[varname[1]]=temp1[0][1]
                            elif re.search(r"NUMBR", temp1[0][0]):
                                symbol_table[varname[1]]= temp1[0][1]
                            elif re.search(r"NUMBAR", temp1[0][0]):
                                symbol_table[varname[1]]= temp1[0][1]
                            elif re.search(r"arithmetic_operator", temp1[0][0]):                       
                                temp= temp1.copy()
                        
                                symbol_table[varname[1]]=self.arithmetic_expression(temp)
                                print(f"SYMBOL TABLE {symbol_table}")
                            elif re.search(r"comparison_operator",temp1[0][0]):
                                temp= temp1.copy()
                                val= self.comparison(temp)
                                symbol_table[varname[1]]= val[1]
                            elif re.search(r"boolean_operator",temp1[0][0]):
                                temp= temp1.copy()
                                val= self.boolean_expression(temp)
                                symbol_table[varname[1]]= val[1]
                            elif re.search(r"concatenation",temp1[0][0]):
                                temp= temp1.copy()
                                val = self.concat(temp)
                                symbol_table[varname[1]]= val[1]
                            elif temp1[0][1]== "MAEK A" or temp1[0][1]=="IS NOW A":
                                #Check if the 2nd variable exists
                                if temp1[1][1]!=varname[1]:
                                    print("SYNTAX: ERROR")
                                    exit()
                                #Checking what data type to convert to
                                if temp1[2][1]=="TROOF":
                                    #Numerical cases
                                    if isinstance( symbol_table[temp1[1][1]],int) or isinstance( symbol_table[temp1[1][1]],float):
                                        x= int(symbol_table[temp1[1][1]])
                                        if x>0:
                                            symbol_table[temp1[1][1]]= "WIN"
                                        else:
                                            symbol_table[temp1[1][1]]= "FAIL"

                                    #Typecasting of numerical strings
                                    elif  isinstance(symbol_table[temp1[1][1]],str):
                                        if symbol_table[temp1[1][1]].isdigit():
                                            x= int(symbol_table[temp1[1][1]])
                                            if x>0:
                                                symbol_table[temp1[1][1]]= "WIN"
                                            else:
                                                symbol_table[temp1[1][1]]= "FAIL"
                                        else:
                                            try:
                                                x=float(symbol_table[temp1[1][1]])
                                            except ValueError:
                                                print("Cannot be converted to TROOF")
                                                exit()
                                elif temp1[2][1]=="NUMBAR":
                                    if isinstance( symbol_table[temp1[1][1]],int) or isinstance( symbol_table[temp1[1][1]],float):
                                        symbol_table[temp1[1][1]]= float(symbol_table[temp1[1][1]])
        

                                    #Typecasting of numerical strings
                                    elif isinstance(symbol_table[temp1[1][1]],str):
                                        if symbol_table[temp1[1][1]].isdigit():
                                            symbol_table[temp1[1][1]]= float(symbol_table[temp1[1][1]])
                                    else:
                                        print("ERROR: Cannot be converted to TROOF")

                                elif temp1[2][1]=="NUMBR":
                                    if isinstance( symbol_table[temp1[1][1]],float):
                                        symbol_table[temp1[1][1]]= int(symbol_table[temp1[1][1]])
                                    elif temp1[1][0]== "TROOF":
                                        if temp1[1][1]=="WIN":
                                            symbol_table[temp1[1][1]]=1
                                        else:
                                            symbol_table[temp1[1][1]]=0
                                    elif isinstance(symbol_table[temp1[1][1]],str):
                                        if symbol_table[temp1[1][1]].isdigit():
                                            symbol_table[temp1[1][1]]=int(symbol_table[temp1[1][1]])
                                        else:
                                            try:
                                                symbol_table[temp1[1][1]]= float(symbol_table[temp1[1][1]])
                                            except ValueError:
                                                print("ERROR: Cannot be converted to NUMBR")
                                elif temp1[2][1]=="NUMBAR":
                                    if isinstance(symbol_table[temp1[1][1]],int):
                                        symbol_table[temp1[1][1]]= float(symbol_table[temp1[1][1]])
                                    elif temp1[1][0]== "TROOF":
                                        if temp1[1][1]=="WIN":
                                            symbol_table[temp1[1][1]]=float(1)
                                        else:
                                            symbol_table[temp1[1][1]]=float(0)

                    else:
                        print("ERROR: Invalid Variable name")
                        exit()
                else:
                    print("ERROR: Missing Argument")
                    exit()
            elif re.search(r"input", self.tokens[0][0]):
                #Check if variable 
                
                if self.tokens[1][0]=="variable":
                    symbol_table[self.tokens[1][1]] = str(input())
            elif re.search(r"comparison_operator", self.tokens[0][0]):
                print(self.index)
                temp= self.tokens.copy()
                val= self.comparison(temp)
                symbol_table["IT"]= val[1]
                
        if self.tokens[0][1]=="YA RLY":
            if symbol_table["IT"] == "WIN":
                ifelse_flag=1
                print("EXECUTING TRUE")
            else:
                print("NOT EXECUTING TRUE")
                ifelse_flag=0
        elif self.tokens[0][1]== "NO WAI":
            if symbol_table["IT"] == "FAIL":
                ifelse_flag=1
                print("EXECUTING FALSE")
            else:
                print("NOT EXECUTING FALSE")
                ifelse_flag=0
        elif self.tokens[0][1]== "OIC":
            ifelse_flag=1 # Set up ifelse flag again sop parser doesnt skip
        
            





            