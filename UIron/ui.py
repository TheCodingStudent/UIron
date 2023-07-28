import re
import ttkbootstrap as ttk
from tkinter import filedialog
from ttkbootstrap.dialogs import Messagebox

class UiError(Exception):
    ...


class StatusBar(ttk.Frame):
    def __init__(self, master: ttk.Frame, raise_notification=True, **kwargs):
        super().__init__(master, **kwargs)

        # PROPERTIES
        self.base_string = 'Ready to continue...'
        self.text = ttk.StringVar()
        self.text_label = ttk.Label(self, textvariable=self.text)
        self.text_label.pack(anchor='w', padx=10)
        self.raise_notification = raise_notification
        self.reset()
    
    def raise_notification(self, text: str, type_: str) -> None:
        """Raises a notificacion, is a template"""
        style = 'danger' if type_ == 'error' else type_
        self.config(bootstyle=style)
        self.text_label.config(bootstyle=f'{style}-inverse')
        self.text.set(text)
        if not self.raise_notification: return self.reset()
        notification = getattr(Messagebox, f'show_{type_}')
        notification(text, title=type_.title(), parent=self.master)
        self.reset()

    def warning(self, text: str) -> None:
        """Changes the bar and raises a warning notification"""
        self.raise_notification(text, 'warning')
    
    def error(self, text: str) -> None:
        """Changes the bar and raises a warning notification"""
        self.raise_notification(text, 'error')
    
    def info(self, text: str) -> None:
        """Changes the bar and raises a warning notification"""
        self.raise_notification(text, 'info')
    
    def reset(self):
        """Restores the status bar"""
        self.text.set(self.base_string)
        self.config(bootstyle='secondary')
        self.text_label.config(bootstyle='secondary-inverse')
    
    def set(self, text: str) -> None:
        """Changes the status bar text"""
        self.text.set(text)
        self.base_string = text


class FormFrame(ttk.Frame, ttk.LabelFrame):
    def __init__(
            self, master: ttk.Frame|ttk.Window, text: str='', **kwargs
    ):
        if not text: ttk.Frame.__init__(self, master, **kwargs)
        else: ttk.LabelFrame.__init__(self, master, text=text, **kwargs)

        self.row = 0
        self.inputs = {}
    
    def add_widget(self, name: str, text: str, widget, sticky: str='w', **kwargs) -> object:
        ttk.Label(self, text=text).grid(row=self.row, column=0, sticky=sticky)
        new_widget = widget(self, **kwargs)
        new_widget.grid(row=self.row, column=1, sticky='ew')
        self.inputs[name] = new_widget
        self.row += 1
        return new_widget

    def add_entry(self, name: str, text: str, sticky: str='w', **kwargs) -> ttk.Entry:
        return self.add_widget(name, text, ttk.Entry, sticky=sticky, **kwargs)

    def add_combobox(self, name: str, text: str, sticky: str='w', **kwargs) -> ttk.Combobox:
        combobox = self.add_widget(name, text, ttk.Combobox, sticky=sticky, **kwargs)
        if kwargs.get('values', []): combobox.current(0)
        return combobox

    def __getitem__(self, key: str) -> object:
        if not key in self.inputs: raise UiError(f'Attribute "{key}" does not exist')
        return self.inputs[key].get()


class PathEntry(ttk.Frame):
    def __init__(
            self, master: ttk.Frame|ttk.Window, text: str='Select path',
            ask: str='directory', width: int=20, **kwargs
    ):
        super().__init__(master, **kwargs)

        self.ask = getattr(filedialog, f'ask{ask}')

        self.entry = ttk.Entry(self, state='readonly', width=width)
        self.entry.pack(side='left', expand=True, fill='x')

        self.button = ttk.Button(self, text=text, command=self.command)
        self.button.pack(padx=(5, 0))
    
    def command(self) -> None:
        if not (path := self.ask()): return
        self.set(path)
    
    def set(self, path: str) -> None:
        self.entry.config(state='normal')
        self.entry.delete(0, 'end')
        self.entry.insert(0, path)
        self.entry.config(state='disabled')

    def get(self) -> str:
        return self.entry.get()


class RegexEntry(ttk.Entry):
    def __init__(
            self, master: ttk.Frame|ttk.Window, regex: str='*', width: int=20,
            invalid_message: str='Invalid input...', show_message: bool=True, **kwargs
    ):
        super().__init__(master, **kwargs)

        self.regex = regex
        self.show_message = show_message
        self.invalid_message = invalid_message

        self.entry = ttk.Entry(self, width=width)
        self.entry.pack(fill='x')
        self.message = ttk.StringVar()
        self.label = ttk.Label(self, textvariable=self.message, anchor='center', bootstyle='danger')

        self.entry.bind('<FocusIn>', self.check_regex)
        self.entry.bind('<KeyRelease>', self.check_regex)
        self.entry.bind('<FocusOut>', self.reset)
    
    def reset(self, *_) -> None:
        self.label.pack_forget()
        self.message.set(value='')
        self.entry.config(bootstyle='default')
    
    def check_regex(self, *_) -> None:
        if re.match(self.regex, self.get()): return self.reset()
        self.message.set(value=self.invalid_message)
        self.entry.config(bootstyle='danger')
        if self.show_message: self.label.pack(fill='x')
    
    def get(self) -> str:
        return self.entry.get()

    def set(self, value: str) -> None:
        self.entry.delete(0, 'end')
        self.entry.insert(0, value)