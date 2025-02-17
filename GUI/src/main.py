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
	# Notebook #
	#----------#
	notebook = ttk.Notebook(root)
	notebook.pack(expand=True, fill='both')
	file_tab = my_gui.notebook.Tab(notebook, "  File", 'file.png')
	signup_tab = my_gui.notebook.Tab(notebook, "  SignUp", 'key.png').hide()
	login_tab = my_gui.notebook.Tab(notebook, "  Login", 'key.png').hide()
	password_tab = my_gui.notebook.Tab(notebook, "  Password", 'key.png').hide()
	database_tab = my_gui.notebook.Tab(notebook, "  Database", 'list.png').hide()
	entry_tab = my_gui.notebook.Tab(notebook, "  Entry", 'entry.png').hide()
	
	#-----------#
	# Tab: File #
	#-----------#


	#-------------#
	# Tab: Signup #
	#-------------#
	

	#------------#
	# Tab: Login #
	#------------#
	
	
	#---------------#
	# Tab: Password #
	#---------------#
	
	
	#---------------#
	# Tab: Database #
	#---------------#
	
	
	#------------#
	# Tab: Entry #
	#------------#


	#----------#
	# MainLoop #
	#----------#
	root.mainloop()


if __name__ == '__main__':
	app()
