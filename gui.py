# -*- coding: utf-8 -*-
"""
:::::::::::::::::::NOTEPAD:::::::::::::::::::

		
This code defines a Kivy App called MyApp, which builds a MyGridLayout that 
contains two labels, two text inputs, and a button. When the button is pressed, 
it triggers the press method, which gets the text from the text inputs and prints 
a message to the console. To run this code, save it in a file (e.g., myapp.py) 
and run it with python myapp.py. This should open a window with the GUI.


"""

# Kivy-Related Imports
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy import utils
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout

# imports from my other .py files
import database
from analyze import Allowables, Stats
stat=Stats()
allow=Allowables()

# other imports:
import os
import pandas as pd
from datetime import datetime

# colors
cool_gray_1 = utils.get_color_from_hex("#D9D9D6")
cool_gray_5 = utils.get_color_from_hex("#B1B3B3")
black = utils.get_color_from_hex("#000000")
white = utils.get_color_from_hex("#FFFFFF")
cool_gray_11 = utils.get_color_from_hex("#53565A")
yellow_115 = utils.get_color_from_hex("#FBDC3E")
orange_159 = utils.get_color_from_hex("#CB6015")

# file folders & filepaths:
logo_path = os.path.join(os.getcwd(),"_assets","logo.png")
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')





# app - page 1
class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 3
        self.padding = 50 # set padding to 50 pixels
        self.spacing = 20 # set spacing between widgets to 20 pixels
        self.row_default_height=50
        self.col_default_width = 150
        
        
        self.add_widget(Label(text='Databases',
                              font_size=40,
                              color=black,
                              bold=True))
        self.add_widget(Label(text='Reports',
                              font_size=40,
                              color=black,
                              bold=True))
        
        # open databases
        button1 = Button(text='Update Summary Databases',
                 size_hint=(0.3, 0.3),
                 font_size=15,
                 pos_hint={'center_x': 0.5, 'center_y': 0.5})
        button1.bind(on_press=self.on_button1_press)
        self.add_widget(button1)
    
        
        button2 = Button(text='Calculate Material Allowables (A,B Basis)',
                 size_hint=(0.3, 0.3),
                 font_size=15,
                 pos_hint={'center_x': 0.5, 'center_y': 0.5})
        button2.bind(on_press=self.on_button2_press)
        self.add_widget(button2)        

    
    # open databases   
    def on_button1_press(self, instance):
        database.save_results_db()
        print("New Databases Generated")
        

    # generate a, b basis allowables
    def on_button2_press(self, instance):
        data = database.load_results_db()
        results = allow.a_b_basis(data,["Condition","Method"])
        
        # export to Excel
        
        with pd.ExcelWriter(rf'Exports/a-b-basis - {current_time}.xlsx') as writer:
            for material, props_data in results.items():
                for prop, df in props_data.items():
                    sheet_name = f"{material}_{prop}"
                    df.to_excel(writer, sheet_name=sheet_name)
        print("a-b-basis.xlsx generated in 'Exports' folder")
        return results


# app - putting them all together
class MyApp(App):
    def build(self):
        Window.clearcolor = white
        layout = BoxLayout(orientation='vertical',
                           spacing=10,
                           padding=10)
        rl = RelativeLayout()
        logo = AsyncImage(source=logo_path,
                          size_hint=(None, None),
                          size=(2000, 2000),
                          height=200,
                          pos_hint={'center_x': 0.5, 'center_y': 0.5})
        rl.add_widget(logo)
        layout.add_widget(rl)
        
        layout.add_widget(MyGridLayout())
        
        return layout


if __name__ == '__main__':
    MyApp().run()