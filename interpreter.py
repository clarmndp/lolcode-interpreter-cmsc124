"""
# LOLCODE Interpreter written in Python
    
    Authors:
        Diño, John Matthew D.
        Mandap, Clarence P.
        Pore, Richmond Michael B.

    Components/ modules:
        lexer.py - Handles tokenization and lexical analysis
        interpreter.py - Ties all components together and handles program execution

    GUI Framework:
        Kivy (https://kivy.org/)
"""
# Kivy functions used
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# Python functions used
import sys
from io import StringIO
import re

# Lexer class from lexer.py
from lexer import Lexer  # import the Lexer class

# symbol table
symbol_table = {}



class MainWindow(App):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.current_file = None
        self.output_buffer = StringIO()

        self.current_line_index = 0  # track the current line index
        self.lines = []  # store lines from the file
        self.tokens_output = ""  # store the tokens for display
        self.tokens_display = TextInput(readonly=True, multiline=True)  # add tokens display (lexeme table)
        self.lexer = Lexer()  # create the lexer instance here

    # function to create main interpreter UI
    def build(self):
        layout = FloatLayout()

        # File Explorer
        file_chooser = FileChooserListView(on_submit=self.load_file)  # FileChooser object for the File Explorer
        file_chooser.size_hint = (0.3, 0.5)
        file_chooser.pos_hint = {'x': 0, 'top': 1} 
        layout.add_widget(file_chooser)

        # Text Editor
        self.text_editor = TextInput(multiline=True, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        self.text_editor.size_hint = (0.3, 0.5)
        self.text_editor.pos_hint = {'x': 0.3, 'top': 1}
        layout.add_widget(self.text_editor)

        # Save Button for Text Editor
        save_button = Button(text='Save', size_hint=(0.3, None), height=50)
        save_button.pos_hint = {'x': 0.3, 'y': 0.5}
        save_button.bind(on_press=self.save_file)
        layout.add_widget(save_button)

        # Lexeme Table
        self.tokens_display.size_hint = (0.3, 0.5)
        self.tokens_display.pos_hint = {'x': 0.6, 'top': 1}
        layout.add_widget(self.tokens_display)

        # Console
        console_section = BoxLayout(orientation='vertical', size_hint=(1, 0.5), pos_hint={'x': 0, 'y': 0})
        self.console_output = TextInput(readonly=True, multiline=True)  # output area
        console_section.add_widget(self.console_output)  # add output area to Console
        
        # Run/Execute Button for Console
        run_button = Button(text='Execute', size_hint_y=None, height=50)
        run_button.bind(on_press=self.run_lolcode)  # Bind the run button to the run_lolcode method
        console_section.add_widget(run_button)  # add a run button to Console
        layout.add_widget(console_section)  # Add the console section to the layout

        return layout
    
    # File Explorer functions
    def load_file(self, instance, selection, touch=None, **kwargs):
        if selection:  # Check if a file is selected
            self.current_file = selection[0]
            with open(self.current_file, 'r') as file:  # Open the selected file
                self.text_editor.text = file.read()  # Load contents to the text editor

    def save_file(self, instance):
        if self.current_file:
            with open(self.current_file, 'w') as file:  # Open in write mode
                file.write(self.text_editor.text)  # Save the contents to the file

    # Main LOLCODE Interpreter
    def interpreter(self, filename):
        # Check if the file extension is .lol
        if not filename.endswith('.lol'):
            # Output: Error message
            self.console_output.text += "Error: File must have '.lol' extension\n"
            return
        try:
            with open(filename, 'r') as file:
                # Read the first line and check for HAI
                starting = file.readline().strip()
                
                if starting != "HAI":
                    # Output: Error
                    self.console_output.text += "Error: Invalid Starting Keyword\n"
                    return

                self.lines = file.readlines()  # Read all lines into a list
                self.current_line_index = 0  # Reset line index

                # create an instance of the Lexer
                lexer = Lexer()

                # Tokenize each line and store the tokens
                self.tokens = []
                for line in self.lines:
                    tokens = lexer.definer(line.strip())  # Tokenize the line
                    self.tokens_output += "\n".join([f"{token.type}: {token.value}" for token in tokens if token.type != "single_line_comment"]) + "\n"  # Collect tokens, Skipping comments
                    self.tokens_display.text = self.tokens_output  # Update the Lexeme Table

                # Start executing lines
                self.execute_next_line()

        except FileNotFoundError:
            self.console_output.text += f"Error: Could not find file '{filename}'\n"

    def execute_next_line(self):
        # Go through each line
        while self.current_line_index < len(self.lines):
            line = self.lines[self.current_line_index].strip()  # Removes the white spaces around the line
            if line:
                tokens = self.lexer.definer(line)  # Use the lexer instance
                if any(token.type == "arithmetic_operator" for token in tokens):
                    self.handle_arithmetic(tokens)  # Handle arithmetic operations
            
            # Evaluate keywords/ identifiers
            if line:
                
                # VISIBLE
                if line.startswith("VISIBLE"):
                    tokenized = line.split("VISIBLE ")
                    tokenized[0] = "VISIBLE"
                    if tokenized[1].startswith("\""):  # String literal printing
                        tokenized[1] = tokenized[1].strip("\"")
                        self.console_output.text += tokenized[1] + "\n"
                    else:
                        # Handle case for arithmetic expressions
                        if "SUM OF" in tokenized[1] or "DIFF OF" in tokenized[1] or "PRODUKT OF" in tokenized[1] or "QUOSHUNT OF" in tokenized[1] or "MOD OF" in tokenized[1]:
                            result = self.handle_arithmetic(self.lexer.definer(tokenized[1]))
                            self.console_output.text += str(result) + "\n"
                        # Valid variable
                        elif tokenized[1] in symbol_table.keys():
                            self.console_output.text += str(symbol_table[tokenized[1]]) + "\n"
                        else:
                            # Output: Error
                            self.console_output.text += f"Variable {tokenized[1]} does not exist in the dictionary\n"
                
                # I HAS A
                elif line.startswith("I HAS A"):
                    tokenized = line.split("I HAS A ")[1].strip()  # Get the variable declaration elementw
                    var_name, var_value = tokenized.split(" ITZ ") if " ITZ " in tokenized else (tokenized, None)
                    if re.match(r"^[A-Za-z]", var_name):  # Valid variable name
                        symbol_table[var_name] = var_value if var_value else None  # Assign value
                
                # ITZ
                elif line.startswith("ITZ"):
                    tokenized = line.split("ITZ ")
                    if len(tokenized) == 2:
                        var_name = tokenized[0].strip()
                        value = tokenized[1].strip()
                        # Handle assignment for WIN and FAIL
                        if value == "WIN":
                            symbol_table[var_name] = "WIN"
                        elif value == "FAIL":
                            symbol_table[var_name] = "FAIL"
                
                # GIMMEH
                elif line.startswith("GIMMEH"):
                    tokenized = line.split("GIMMEH ")
                    tokenized[0] = "GIMMEH"
                    if tokenized[1] not in symbol_table.keys():
                        self.console_output.text += f"Variable {tokenized[1]} is not known\n"
                        return
                    else:
                        self.prompt_for_input(tokenized[1])  # Prompt for input (popup)
                        return  # break out of the loop to wait for input
                                # this stops the interpreter from executing further lines
                
                # Boolean operators
                elif "BOTH OF" in line:
                    # Handle BOTH OF logic
                    operands = line.split("BOTH OF")
                    if len(operands) == 2:
                        left = operands[0].strip()
                        right = operands[1].strip()
                        result = (self.evaluate_expression(left) and self.evaluate_expression(right))
                elif "EITHER OF" in line:
                    # Handle EITHER OF logic
                    operands = line.split("EITHER OF")
                    if len(operands) == 2:
                        left = operands[0].strip()
                        right = operands[1].strip()
                        result = (self.evaluate_expression(left) or self.evaluate_expression(right))
                elif "WON OF" in line:
                    # Handle WON OF logic
                    operands = line.split("WON OF")
                    if len(operands) == 2:
                        left = operands[0].strip()
                        right = operands[1].strip()
                        result = (self.evaluate_expression(left) ^ self.evaluate_expression(right))
                elif "NOT" in line:
                    # Handle NOT logic
                    operand = line.split("NOT")[1].strip()
                    result = not self.evaluate_expression(operand)

            self.current_line_index += 1  # move to the next line

    # Arithmetic operation logic
    def handle_arithmetic(self, tokens):
        # Check if the tokens represent an arithmetic operation
        if len(tokens) == 4 and tokens[2].value == "AN":  # Ensure the format is OPERATOR OPERAND1 AN OPERAND2
            operator = tokens[0].value
            operand1 = self.evaluate_operand(tokens[1].value)  # Evaluate the first operand
            operand2 = self.evaluate_operand(tokens[3].value)  # Evaluate the second operand
            
            # Convert operands to int or float
            operand1 = int(operand1)
            operand2 = int(operand2)

            if operator == "SUM OF":
                result = operand1 + operand2
            elif operator == "DIFF OF":
                result = operand1 - operand2
            elif operator == "PRODUKT OF":
                result = operand1 * operand2
            elif operator == "QUOSHUNT OF":
                result = operand1 / operand2 if operand2 != 0 else "Error: Division by zero"
            elif operator == "MOD OF":
                result = operand1 % operand2 if operand2 != 0 else "Error: Division by zero"
            else:
                result = "Error: Unknown operator"

            return result

    # Function to check if operand is a variable or num
    def evaluate_operand(self, operand):
        if operand in symbol_table:
            value = symbol_table[operand] if symbol_table[operand] is not None else 0  # Return 0 if variable is None
            return value

    # Boolean evaluation
    def evaluate_expression(self, expression):
        # Evaluate the expression and return a boolean value
        if expression in symbol_table:
            return symbol_table[expression] == "WIN"
        return expression == "WIN"

    # Function to call interpreter function when user runs code
    def run_lolcode(self, instance):
        if self.current_file:  # check if a file is selected
            self.output_buffer = StringIO()
            sys.stdout = self.output_buffer
            
            try:
                # call the interpreter function
                self.interpreter(self.current_file)
            except Exception as e:
                self.console_output.text += f"Error during execution: {str(e)}\n"
        else:
            self.console_output.text += "Error: No file selected.\n"

    # User input popup
    def prompt_for_input(self, variable_name):
        input_box = TextInput(hint_text=f"Enter value for {variable_name}", multiline=False)
        submit_button = Button(text="Submit", size_hint_y=None, height=50)
        cancel_button = Button(text="Cancel", size_hint_y=None, height=50)

        def on_submit(instance):
            value = input_box.text.strip()  # Get input from user
            if value:  # Check if the input is not empty
                symbol_table[variable_name] = value
                popup.dismiss()
                self.current_line_index += 1  # Move to the next line after input
                self.execute_next_line()  # Call function to execute the next line
            else:
                self.console_output.text += "Error: Input cannot be empty.\n"

        def on_cancel(instance):
            popup.dismiss()  # Close popup

        submit_button.bind(on_press=on_submit)
        cancel_button.bind(on_press=on_cancel)

        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_content.add_widget(input_box)
        popup_content.add_widget(submit_button)
        popup_content.add_widget(cancel_button)

        popup = Popup(title="Input Required", content=popup_content, size_hint=(0.8, 0.4))
        popup.open() 

if __name__ == '__main__':
    MainWindow().run()