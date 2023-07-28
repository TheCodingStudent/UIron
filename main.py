import os
import ttkbootstrap as ttk
from UIron.config import Config
from UIron.regex import DECIMAL_NUMBERS, EMAIL
from UIron.ui import FormFrame, PathEntry, RegexEntry


path = os.path.join(os.path.dirname(__file__), 'UIron/data/new.json')
config = Config(path)

window = ttk.Window(themename='darkly')

form = FormFrame(window)
form.add_entry('name', 'Name: ')
form.add_combobox('numbers', 'Numbers: ', values=[1,2,3])
form.add_widget('decimal', 'Decimal number: ', RegexEntry, regex=EMAIL, show_message=False)
form.pack(expand=True, fill='both', padx=10, pady=10)

path = PathEntry(window)
path.pack(fill='x', padx=10, pady=10)
path.button.config(bootstyle='success')

ttk.Button(window, text='Print...', command=lambda: print(form['name'])).pack(fill='x')

window.mainloop()