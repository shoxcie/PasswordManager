import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

import my_gui


#-----------#
# Constants #
#-----------#
WIN_TITLE = "Password Manager"
WIN_MIN_WIDTH, WIN_MIN_HEIGHT = 600, 400
WIN_WIDTH, WIN_HEIGHT = 600, 400

FILE_EXT = 'shxc'
FILE_MAX_SIZE = 1024
DIR_DOCS = os.path.abspath(os.path.join(os.path.expanduser('~'), 'Documents'))


def app():
	#------#
	# Root #
	#------#
	root = tk.Tk()
	root.title(WIN_TITLE)
	root.minsize(WIN_MIN_WIDTH, WIN_MIN_HEIGHT)
	root.geometry(f'{int(WIN_WIDTH)}x{int(WIN_HEIGHT)}')
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
	
	#-------------#
	# File Search #
	#-------------#
	tab_file_search = [f for f in os.listdir(DIR_DOCS) if f.endswith('.shxc')]
	tab_file_reason = ''
	if len(tab_file_search) == 0:
		tab_file_reason = "  Database file not found, please select or create one"
	elif len(tab_file_search) > 1:
		tab_file_reason = "  Multiple database files found, please select one"
	
	#----------#
	# Notebook #
	#----------#
	notebook = ttk.Notebook(root)
	notebook.pack(expand=True, fill='both')
	tab_file = my_gui.notebook.Tab(notebook, tab_file_reason, 'file.png')
	tab_signup = my_gui.notebook.Tab(notebook, "  SignUp", 'key.png').hide()
	tab_login = my_gui.notebook.Tab(notebook, "  Login", 'key.png').hide()
	tab_password = my_gui.notebook.Tab(notebook, "  Password", 'key.png').hide()
	tab_database = my_gui.notebook.Tab(notebook, "  Database", 'list.png').hide()
	tab_entry = my_gui.notebook.Tab(notebook, "  Entry", 'entry.png').hide()
	
	#-----------#
	# Tab: File #
	#-----------#
	tab_file_path = ''
	
	def tab_file_onclick_select():
		nonlocal tab_file_path
		tab_file_path = filedialog.askopenfilename(
			initialdir = DIR_DOCS,
			title="Select the Database File",
			filetypes=[("Shoxcie's Password Manager File", f'*.{FILE_EXT}')]
		)
		if tab_file_path and os.path.getsize(tab_file_path) < FILE_MAX_SIZE:
			tab_file.hide()
			tab_login.show()
	
	def tab_file_onclick_create():
		nonlocal tab_file_path
		tab_file_path = filedialog.asksaveasfilename(
			initialdir = DIR_DOCS,
			title="Name the Database File",
			filetypes=[("Shoxcie's Password Manager File", f'*.{FILE_EXT}')],
			defaultextension=f'{FILE_EXT}',
			confirmoverwrite=True
		)
		if tab_file_path.endswith(f'.{FILE_EXT}'):
			tab_file.hide()
			tab_signup.show()
	
	if tab_file_reason:
		tab_file.show()
	
	ttk.Button(tab_file.frame, text="Select", command=tab_file_onclick_select).pack(
		padx=(WIN_MIN_WIDTH / 3), fill='x', pady=20
	)
	ttk.Button(tab_file.frame, text="Create", command=tab_file_onclick_create).pack(
		padx=(WIN_MIN_WIDTH / 3), fill='x', pady=0
	)
	
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
