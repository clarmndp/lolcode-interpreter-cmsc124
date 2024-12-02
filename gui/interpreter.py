from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import sys
from io import StringIO
import threading
import re
from lexer import Lexer  # import the Lexer class

symbol_table = {}

class MainWindow(App):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.current_file = None
        Window.title = "LOLCODE Interpreter"
        self.output_buffer = StringIO()  # Buffer for capturing output

    def build(self):
        layout = BoxLayout(orientation='horizontal')
        
        # Section 1: File Explorer
        section1 = BoxLayout()
        with section1.canvas:
            Color(0, 0, 0, 1)
            self.bg_rect1 = Rectangle(size=section1.size, pos=section1.pos)
        with section1.canvas.before:
            Color(1, 1, 1, 1)
            self.rect1 = Rectangle(size=section1.size, pos=section1.pos)
        section1.bind(pos=self.update_rect1, size=self.update_rect1)  # update section size to be dynamic
        
        file_chooser = FileChooserListView(on_submit=self.load_file)  # FileChooser object for the File Explorer
        section1.add_widget(file_chooser)  # add file chooser to section 1
        
        # Section 2: Text Editor
        section2 = BoxLayout(orientation='vertical')
        with section2.canvas:
            Color(0, 0, 0, 1)
            self.bg_rect2 = Rectangle(size=section2.size, pos=section2.pos)
        with section2.canvas.before:
            Color(1, 1, 1, 1)
            self.rect2 = Rectangle(size=section2.size, pos=section2.pos)
        section2.bind(pos=self.update_rect2, size=self.update_rect2)
        
        self.text_editor = TextInput(multiline=True, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        section2.add_widget(self.text_editor)  # add a text input for the Text Editor
        
        # Save button for user changes
        save_button = Button(text='Save', size_hint_y=None, height=50)
        save_button.bind(on_press=self.save_file)
        section2.add_widget(save_button)
        
        # Section 3: Console
        section3 = BoxLayout(orientation='vertical')
        with section3.canvas:
            Color(0, 0, 0, 1)
            self.bg_rect3 = Rectangle(size=section3.size, pos=section3.pos)
        with section3.canvas.before:
            Color(1, 1, 1, 1)
            self.rect3 = Rectangle(size=section3.size, pos=section3.pos)
        section3.bind(pos=self.update_rect3, size=self.update_rect3)
        
        self.console_output = TextInput(readonly=True, multiline=True)  # output area
        section3.add_widget(self.console_output)  # add output area to Console
        
        run_button = Button(text='Run LOLCODE', size_hint_y=None, height=50)
        run_button.bind(on_press=self.run_lolcode)  # bind button to run the code
        section3.add_widget(run_button)  # add a run button to Console
        
        layout.add_widget(section1)
        layout.add_widget(section2)
        layout.add_widget(section3)
        return layout

    def load_file(self, filechooser, selection, touch):
        if selection:  # check if a file is selected
            self.current_file = selection[0]
            with open(self.current_file, 'r') as file:  # open the selected file
                self.text_editor.text = file.read()  # load contents to the text editor

    def save_file(self, instance):
        if self.current_file:
            with open(self.current_file, 'w') as file:  # open in write mode
                file.write(self.text_editor.text)  # save the contents to the file

    def update_rect1(self, instance, value):
        self.rect1.pos = instance.pos
        self.rect1.size = instance.size
        self.bg_rect1.pos = instance.pos
        self.bg_rect1.size = instance.size

    def update_rect2(self, instance, value):
        self.rect2.pos = instance.pos
        self.rect2.size = instance.size
        self.bg_rect2.pos = instance.pos
        self.bg_rect2.size = instance.size

    def interpreter(self, filename):
        # We first check if the file extension is .lol
        if not filename.endswith('.lol'):
            self.console_output.text += "Error: File must have '.lol' extension\n"
            return
        
        try:
            with open(filename, 'r') as file:
                # Read the first line and check for HAI
                starting = file.readline().strip()
                
                if starting != "HAI":
                    self.console_output.text += "Error: Invalid Starting Keyword\n"
                    return

                # Proceed to the rest of the LOLCODE file
                for line in file:
                    line = line.strip()  # Removes the white spaces around the line
                    if line:  # Skip empty lines
                        if line.startswith("VISIBLE"):
                            tokenized = line.split("VISIBLE ")
                            tokenized[0] = "VISIBLE"
                            if tokenized[1].startswith("\""):  # String literal printing
                                tokenized[1] = tokenized[1].strip("\"")
                                self.console_output.text += f"{tokenized[1]}\n"
                            else:
                                # Valid variable
                                if tokenized[1] in symbol_table.keys():
                                    self.console_output.text += f"{symbol_table[tokenized[1]]}\n"
                                else:
                                    self.console_output.text += f"Variable {tokenized[1]} does not exist in the dictionary\n"
                        elif line.startswith("I HAS A"):
                            tokenized = line.split("I HAS A ")
                            tokenized.pop(0)
                            tokenized = tokenized[0].split(" ")
                            tokenized.insert(0, "I HAS A")
                            if re.match(r"^[A-Z a-z]", tokenized[1]):  # Valid variable name
                                symbol_table[tokenized[1]] = tokenized[3]
                            else:
                                self.console_output.text += "Variable Error: Not a valid variable name\n"
                        elif line.startswith("GIMMEH"):
                            tokenized = line.split("GIMMEH ")
                            tokenized[0] = "GIMMEH"
                            if tokenized[1] not in symbol_table.keys():
                                self.console_output.text += f"Variable {tokenized[1]} is not known\n"
                                return
                            else:
                                self.prompt_for_input(tokenized[1])  # prompt for input

        except FileNotFoundError:
            self.console_output.text += f"Error: Could not find file '{filename}'\n"

    def run_lolcode(self, instance):
        if self.current_file:  # check if a file is selected
            self.output_buffer = StringIO()
            sys.stdout = self.output_buffer
            
            # call the interpreter function
            self.interpreter(self.current_file)
        else:
            self.console_output.text += "Error: No file selected.\n"

    def update_rect3(self, instance, value):
        self.rect3.pos = instance.pos
        self.rect3.size = instance.size
        self.bg_rect3.pos = instance.pos
        self.bg_rect3.size = instance.size

    def prompt_for_input(self, variable_name):
        # create a popup to get user input
        input_box = TextInput(hint_text=f"Enter value for {variable_name}", multiline=False)
        submit_button = Button(text="Submit", size_hint_y=None, height=50)
        cancel_button = Button(text="Cancel", size_hint_y=None, height=50)

        def on_submit(instance):
            value = input_box.text.strip()  # get input from user
            if value:  # Check if the input is not empty
                symbol_table[variable_name] = value
                self.console_output.text += f"Value for {variable_name} set to {value}\n"
                popup.dismiss()
            else:
                self.console_output.text += "Error: Input cannot be empty.\n"

        def on_cancel(instance):
            popup.dismiss()  # close popup

        submit_button.bind(on_press=on_submit)
        cancel_button.bind(on_press=on_cancel)

        # create the popout layout
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_content.add_widget(input_box)
        popup_content.add_widget(submit_button)
        popup_content.add_widget(cancel_button)

        popup = Popup(title="Input Required", content=popup_content, size_hint=(0.8, 0.4))
        popup.open()

if __name__ == '__main__':
    MainWindow().run()