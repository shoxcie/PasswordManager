import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from string import punctuation
import os

import my_gui


#-----------#
# Constants #
#-----------#
WIN_TITLE = "Password Manager"
WIN_MIN_WIDTH, WIN_MIN_HEIGHT = 600, 450
WIN_WIDTH, WIN_HEIGHT = 600, 450

FILE_EXT = 'shxc'
FILE_MAX_SIZE = 1024
DIR_DOCS = os.path.abspath(os.path.join(os.path.expanduser('~'), 'Documents'))

PSWD_MIN_SIZE = 8


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
	tab_signup_show_bool = False
	
	def tab_signup_onclick_show():
		nonlocal tab_signup_show_bool
		tab_signup_show_bool = not tab_signup_show_bool
		
		if tab_signup_show_bool:
			tab_signup_entry.config(show='')
			tab_signup_entry_confirm.config(show='')
		else:
			tab_signup_entry.config(show='*')
			tab_signup_entry_confirm.config(show='*')
	
	def tab_signup_onclick_confirm():
		pswd0 = tab_signup_entry.get()
		pswd1 = tab_signup_entry_confirm.get()
		
		if pswd0 != pswd1:
			messagebox.showerror("Error", "Passwords do not match")
		elif len(pswd0) < PSWD_MIN_SIZE:
			messagebox.showerror("Error", f"Password is too short (< {PSWD_MIN_SIZE})")
		elif not any(char.isdigit() for char in pswd0):
			messagebox.showerror("Error", "Password must contain at least one digit")
		elif not any(char.isupper() for char in pswd0):
			messagebox.showerror("Error", "Password must contain at least one uppercase letter")
		elif not any(char in punctuation for char in pswd0):
			messagebox.showerror("Error", "Password must contain at least one special character")
		
		# TODO: Create a new database file and encrypt it with the pswd0
	
	ttk.Button(tab_signup.frame, text="Toggle View", command=tab_signup_onclick_show).pack(
		padx=(WIN_MIN_WIDTH / 3), fill='x', pady=20
	)
	
	tab_signup_entry_frame = ttk.Frame(tab_signup.frame)
	tab_signup_entry_frame.pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', pady=0
	)
	
	ttk.Label(tab_signup_entry_frame, text="Password:").pack(anchor='w')
	tab_signup_entry = ttk.Entry(tab_signup_entry_frame, show='*')
	tab_signup_entry.pack(fill='x')
	
	ttk.Label(tab_signup_entry_frame, text="Repeat Password:").pack(anchor='w')
	tab_signup_entry_confirm = ttk.Entry(tab_signup_entry_frame, show='*')
	tab_signup_entry_confirm.pack(fill='x')
	
	ttk.Button(tab_signup.frame, text="Confim", command=tab_signup_onclick_confirm).pack(
		padx=(WIN_MIN_WIDTH / 3), fill='x', pady=30
	)
	
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
