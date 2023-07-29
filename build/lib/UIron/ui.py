import re
import types
from typing import Any
from PIL import ImageTk
import ttkbootstrap as ttk
from tkinter import filedialog
from PIL import Image as pil_image
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs import Messagebox

class UIError(Exception):
    ...


class Column(ttk.Frame):
    def __init__(self, master: ttk.Frame|ttk.Window, align: str='', **kwargs):
        super().__init__(master, **kwargs)
    
    def pack(self, **kwargs) -> None:
        for i, children in enumerate(self.winfo_children()):
            children.grid(row=i, column=0, sticky='ew')
        return super().pack(**kwargs)


class Row(ttk.Frame):
    def __init__(self, master: ttk.Frame|ttk.Window, align: str='', **kwargs):
        super().__init__(master, **kwargs)
    
    def pack(self, **kwargs) -> None:
        for i, children in enumerate(self.winfo_children()):
            children.grid(row=0, column=i)
        return super().pack(**kwargs)


class Draggable:
    def __new__(cls, widget, *args, master=None, just_droppable: bool=False, **kwargs):
        widget = widget(master, *args, **kwargs)
        cls.__init__(cls, widget, just_droppable)
        return widget

    def __init__(self, widget, just_droppable: bool):
        self.widget = widget
        self.widget.bind('<Button-1>', self.on_drag_start)
        self.widget.bind('<B1-Motion>', self.on_drag_motion)
        self.widget.bind('<ButtonRelease-1>', self.on_drag_stop)

        self.widget.just_droppable = just_droppable
        self.widget.original_place = getattr(self.widget, 'place')
        self.widget.place = types.MethodType(self.place, self.widget)
        self.widget.origin_x, self.widget.origin_y = None, None

    def place(self, *args, **kwargs) -> None:
        self.original_place(*args, **kwargs)
        if self.origin_x is None: self.origin_x = self.winfo_x()
        if self.origin_y is None: self.origin_y = self.winfo_y()

    def on_drag_start(event) -> None:
        event.widget.lift()
        event.widget._drag_start_x = event.x
        event.widget._drag_start_y = event.y
        event.widget._origin_start_x = event.widget.winfo_x()
        event.widget._origin_start_y = event.widget.winfo_y()
    
    def on_drag_stop(event) -> None:
        event.widget.lower()
        widget_below = event.widget.winfo_containing(event.x_root, event.y_root)
        if event.widget.just_droppable:
            if not hasattr(widget_below, '_droppable'):
                event.widget.lower()
                return event.widget.place(x=event.widget.origin_x, y=event.widget.origin_y)
        
            x, y = widget_below.winfo_x(), widget_below.winfo_y()
            width, height = widget_below.winfo_width(), widget_below.winfo_height()
            widget_width, widget_height = event.widget.winfo_width(), event.widget.winfo_height()

            event.widget.place(x=x+(width-widget_width)/2, y=y+(height-widget_height)/2)
            return event.widget.lift()
        
        x, y = event.x, event.y
        widget_width, widget_height = event.widget.winfo_width(), event.widget.winfo_height()
        event.widget.place(x=x-widget_width/2, y=y-widget_height/2)
        event.widget.lift()

    def on_drag_motion(event):
        x = event.widget.winfo_x() - event.widget._drag_start_x + event.x
        y = event.widget.winfo_y() - event.widget._drag_start_y + event.y
        event.widget.place(x=x, y=y)


class Droppable:
    def __new__(cls, widget, master=None, **kwargs):
        widget = widget(master, **kwargs)
        cls.__init__(cls, widget)
        return widget

    def __init__(self, widget):
        self.widget = widget
        self.widget._droppable = True

        self.widget.original_place = getattr(self.widget, 'place')
        self.widget.place = types.MethodType(self.place, self.widget)
    
    def place(self, *args, **kwargs):
        self.original_place(*args, **kwargs)
        self.origin_x, self.origin_y = self.winfo_x(), self.winfo_y()


class StatusBar(ttk.Frame):
    def __init__(self, master: ttk.Frame, raise_notification=True, **kwargs):
        super().__init__(master, **kwargs)

        # PROPERTIES
        self.base_string = 'Ready to continue...'
        self.text = ttk.StringVar()
        self.text_label = ttk.Label(self, textvariable=self.text)
        self.text_label.pack(anchor='w', padx=10)
        self._raise_notification = raise_notification
        self.reset()
    
    def raise_notification(self, text: str, type_: str) -> None:
        """Raises a notificacion, is a template"""
        style = 'danger' if type_ == 'error' else type_
        self.config(bootstyle=style)
        self.text_label.config(bootstyle=f'{style}-inverse')
        self.text.set(text)
        if not self._raise_notification: return self.reset()
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

    def add_widget(self, name: str, text: str, widget, sticky: str='w', **kwargs) -> object:
        ttk.Label(self, text=text).grid(row=self.row, column=0, sticky=sticky)
        new_widget = widget(self, **kwargs)
        new_widget.grid(row=self.row, column=1, sticky='ew')
        setattr(self, name, new_widget)
        self.row += 1
        return new_widget

    def add_entry(self, name: str, text: str, sticky: str='w', **kwargs) -> ttk.Entry:
        return self.add_widget(name, text, ttk.Entry, sticky=sticky, **kwargs)

    def add_combobox(self, name: str, text: str, sticky: str='w', **kwargs) -> ttk.Combobox:
        combobox = self.add_widget(name, text, ttk.Combobox, sticky=sticky, **kwargs)
        if kwargs.get('values', []): combobox.current(0)
        return combobox

    def __getitem__(self, key: str) -> object:
        if not hasattr(self, key): raise UIError(f'Attribute "{key}" does not exist')
        return getattr(self, key).get()


class PathEntry(ttk.Frame):
    def __init__(
            self, master: ttk.Frame|ttk.Window, text: str='Select path',
            ask: str='directory', width: int=20, command: object=None,
            **kwargs
    ):
        super().__init__(master, **kwargs)

        self.ask = getattr(filedialog, f'ask{ask}')
        self.command = command

        self.entry = ttk.Entry(self, state='readonly', width=width)
        self.entry.pack(side='left', expand=True, fill='x')

        self.button = ttk.Button(self, text=text, command=self.on_click)
        self.button.pack(padx=(5, 0))
    
    def on_click(self) -> None:
        if not (path := self.ask()): return
        self.set(path)
        if self.command: self.command()
    
    def set(self, path: str) -> None:
        self.entry.config(state='normal')
        self.entry.delete(0, 'end')
        self.entry.insert(0, path)
        self.entry.config(state='disabled')

    def get(self) -> str:
        return self.entry.get()


class RegexEntry(ttk.Entry):
    def __init__(
            self, master: ttk.Frame|ttk.Window, regex: str='*',
            invalid_message: str='Invalid input...', show_message: bool=True, **kwargs
    ):
        super().__init__(master, **kwargs)

        self.regex = regex
        self.show_message = show_message
        self.invalid_message = invalid_message

        self.message = ttk.StringVar()
        self.label = ttk.Label(self, textvariable=self.message, anchor='center', bootstyle='danger')

        self.bind('<FocusIn>', self.check_regex)
        self.bind('<KeyRelease>', self.check_regex)
        self.bind('<FocusOut>', self.reset)
    
    def ok(self) -> bool:
        self.check_regex()
        return self._ok

    def reset(self, *_) -> None:
        self.label.pack_forget()
        self.message.set(value='')
        self.config(bootstyle='default')
    
    def check_regex(self, *_) -> None:
        self._ok = re.match(self.regex, self.get())
        if self._ok: return self.reset()
        self.message.set(value=self.invalid_message)
        self.config(bootstyle='danger')
        if self.show_message: self.label.pack(fill='x')

    def set(self, value: str) -> None:
        self.delete(0, 'end')
        self.insert(0, value)


class Image(ttk.Label):
    def __init__(self, master: ttk.Frame|ttk.Window, path: str='', **kwargs):
        super().__init__(master, **kwargs)
        if path: self.config(image=path)
    
    def set_image(self, image, scale: float=1) -> None:
        self._image = image
        self.width, self.height = self._image.size
        self.image = ImageTk.PhotoImage(self._image)
        super().config(image=self.image)
        if scale != 1: self.resize_by(scale)

    def resize(self, width: int=0, height: int=0) -> None:
        if width==0 and height==0: raise UIError('No size provided to resize image...')
        if not width and height: width = int(height*self.width/self.height)
        elif not height and width: height = int(width*self.height/self.width)
        self.set_image(self._image.resize((width, height)))
    
    def resize_by(self, scale: float) -> None:
        width, height = int(self.width * scale), int(self.height * scale)
        self.resize(width, height)

    def config(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'image': self.set_image(pil_image.open(value))
            else: super().config(**{key:value})
    
    def __setitem__(self, key: str, value: Any) -> None:
        if key == 'image': return self.config(image=value)
        return super().__setitem__(key, value)


class MenuButton(ttk.Label):
    def __init__(self, master: ttk.Frame, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = None
        self.hovered = False
        self.clicked = False

        self.color = ttk.Style().theme.colors.bg
        self.hover_color = ttk.Style().theme.colors.info
        self.click_color = ttk.Style().theme.colors.success

        self.tooltip = ToolTip(self, text=kwargs['text'], bootstyle='primary-inverse')
        self.bind('<Enter>', self.enter)
        self.bind('<Leave>', self.leave)
        self.bind('<Button-1>', self.click)
    
    def enter(self, *_) -> None:
        self.hovered = True
        self.update_color()
        self.tooltip.show_tip()
    
    def leave(self, *_) -> None:
        self.hovered = False
        self.update_color()
        self.tooltip.hide_tip()
    
    def click(self, *_) -> None:
        self.clicked = True
        self.update_color()
        self.after(100, self.release)
        if self.command: self.command()
    
    def release(self, *_) -> None:
        self.clicked = False
        self.update_color()
    
    def update_color(self) -> None:
        if self.clicked: self.config(background=self.click_color)
        elif self.hovered: self.config(background=self.hover_color)
        else: self.config(background=self.color)

    def config(self, **kwargs):
        if 'image' in kwargs:
            image = pil_image.open(kwargs['image'])
            self.image = kwargs['image'] = ImageTk.PhotoImage(image)
        return super().config(**kwargs)