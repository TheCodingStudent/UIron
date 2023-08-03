import ttkbootstrap as ttk
from UIron.ui import Row, ImageButton, StatusBar

window = ttk.Window(themename='darkly')

image = ImageButton(window, path='c:/users/lenovo/desktop/dibujos/spider gwen.png')
image.resize_by(0.1)
image.pack(padx=20, pady=20)

# StatusBar(window, theme='info').pack(fill='x', anchor='s')

window.mainloop()