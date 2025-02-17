import tkinter as tk
from tkinter import ttk

import my_gui


#-----------#
# Constants #
#-----------#
TITLE = "Password Manager"
WIDTH_MIN, HEIGHT_MIN = 600, 400
WIDTH, HEIGHT = 600, 400


def app():
	#------#
	# Root #
	#------#
	root = tk.Tk()
	root.title(TITLE)
	root.minsize(WIDTH_MIN, HEIGHT_MIN)
	root.geometry(f'{int(WIDTH)}x{int(HEIGHT)}')
	root.bind('<Control-w>', lambda event: root.destroy())
	
	#-----------#
	# Theme: TK #
	#-----------#
	for option in my_gui.theme.tk:
		root.option_add(*option)
	
	#------------#
	# Theme: TTK #
	#------------#
	style = ttk.Style()
	style.theme_create(themename='black_theme', settings=my_gui.theme.ttk)
	style.theme_use('black_theme')
	
	#----------#
	# MainLoop #
	#----------#
	root.mainloop()


if __name__ == '__main__':
	app()
