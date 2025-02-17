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
WIN_MIN_WIDTH, WIN_MIN_HEIGHT = 700, 550
WIN_WIDTH, WIN_HEIGHT = 700, 550

FILE_EXT = 'shxc'
FILE_MAX_SIZE = 1024
DIR_DOCS = os.path.abspath(os.path.join(os.path.expanduser('~'), 'Documents'))

PSWD_MIN_SIZE = 8


def is_password_strong_enough(password: str, echo: str) -> bool:
	status = False	
	
	if password != echo:
		messagebox.showerror("Error", "Passwords do not match")
	elif len(password) < PSWD_MIN_SIZE:
		messagebox.showerror("Error", f"Password is too short (< {PSWD_MIN_SIZE})")
	elif not any(char.isdigit() for char in password):
		messagebox.showerror("Error", "Password must contain at least one digit")
	elif not any(char.isupper() for char in password):
		messagebox.showerror("Error", "Password must contain at least one uppercase letter")
	elif not any(char in punctuation for char in password):
		messagebox.showerror("Error", "Password must contain at least one special character")
	else:
		status = True
	
	return status


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
	tab_login_reason = ''
	if len(tab_file_search) == 0:
		tab_file_reason = "  Database file not found, please select or create one"
	elif len(tab_file_search) > 1:
		tab_file_reason = "  Multiple database files found, please select one"
	else:
		tab_login_reason = os.path.join(DIR_DOCS, tab_file_search[0])
	
	#----------#
	# Notebook #
	#----------#
	notebook = ttk.Notebook(root)
	notebook.pack(expand=True, fill='both')
	tab_file = my_gui.notebook.Tab(notebook, tab_file_reason, 'file.png').hide()
	tab_signup = my_gui.notebook.Tab(notebook, "  SignUp", 'key.png').hide()
	tab_login = my_gui.notebook.Tab(notebook, f" File \"{tab_login_reason}\"", 'key.png').hide()
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
			tab_signup_entry_echo.config(show='')
		else:
			tab_signup_entry.config(show='*')
			tab_signup_entry_echo.config(show='*')
	
	def tab_signup_onclick_confirm():
		pswd0 = tab_signup_entry.get()
		pswd1 = tab_signup_entry_echo.get()
		
		if is_password_strong_enough(pswd0, pswd1):
			pass
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
	tab_signup_entry_echo = ttk.Entry(tab_signup_entry_frame, show='*')
	tab_signup_entry_echo.pack(fill='x')
	
	ttk.Button(tab_signup.frame, text="Confim", command=tab_signup_onclick_confirm).pack(
		padx=(WIN_MIN_WIDTH / 3), fill='x', pady=30
	)
	
	#------------#
	# Tab: Login #
	#------------#
	tab_login_show_bool = False
	
	def tab_login_onclick_show():
		nonlocal tab_login_show_bool
		tab_login_show_bool = not tab_login_show_bool
		
		if tab_login_onclick_show:
			tab_login_entry.config(show='')
		else:
			tab_login_entry.config(show='*')
	
	def tab_login_onclick_confirm():
		pass
		# TODO: Decrypt the database file with tab_login_entry.get() password
		#	if the password is correct, show main tabs
		#	else, show error message
	
	if not tab_file_reason:
		tab_login.show()
	
	ttk.Button(tab_login.frame, text="Toggle View", command=tab_login_onclick_show).pack(
		padx=(WIN_MIN_WIDTH / 3), fill='x', pady=20
	)
	
	tab_login_entry_frame = ttk.Frame(tab_login.frame)
	tab_login_entry_frame.pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', pady=0
	)
	
	ttk.Label(tab_login_entry_frame, text="Password:").pack(anchor='w')
	tab_login_entry = ttk.Entry(tab_login_entry_frame, show='*')
	tab_login_entry.pack(fill='x')
	
	ttk.Button(tab_login.frame, text="Confim", command=tab_login_onclick_confirm).pack(
		padx=(WIN_MIN_WIDTH / 3), fill='x', pady=30
	)
	
	#---------------#
	# Tab: Password #
	#---------------#
	tab_password_show_bool = False
	
	def tab_password_onclick_show():
		nonlocal tab_password_show_bool
		tab_password_show_bool = not tab_password_show_bool
		
		if tab_password_show_bool:
			tab_password_entry.config(show='')
			tab_password_entry_new.config(show='')
			tab_password_entry_new_echo.config(show='')
		else:
			tab_password_entry.config(show='*')
			tab_password_entry_new.config(show='*')
			tab_password_entry_new_echo.config(show='*')
	
	def tab_password_onclick_confirm():
		pswd0 = tab_password_entry_new.get()
		pswd1 = tab_password_entry_new_echo.get()
		
		if True and is_password_strong_enough(pswd0, pswd1): # TODO: Check if the current password is correct]
			pass
			# TODO: Change the password in the database file
	
	ttk.Button(tab_password.frame, text="Toggle View", command=tab_password_onclick_show).pack(
		padx=(WIN_MIN_WIDTH / 3), fill='x', pady=20
	)
	
	tab_password_entry_frame = ttk.Frame(tab_password.frame)
	tab_password_entry_frame.pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', pady=0
	)
	
	ttk.Label(tab_password_entry_frame, text="Current Password:").pack(anchor='w')
	tab_password_entry = ttk.Entry(tab_password_entry_frame, show='*')
	tab_password_entry.pack(fill='x')
	
	ttk.Label(tab_password_entry_frame, text="New Password:").pack(anchor='w')
	tab_password_entry_new = ttk.Entry(tab_password_entry_frame, show='*')
	tab_password_entry_new.pack(fill='x')

	ttk.Label(tab_password_entry_frame, text="Repeat New Password:").pack(anchor='w')
	tab_password_entry_new_echo = ttk.Entry(tab_password_entry_frame, show='*')
	tab_password_entry_new_echo.pack(fill='x')
	
	ttk.Button(tab_password.frame, text="Confim", command=tab_password_onclick_confirm).pack(
		padx=(WIN_MIN_WIDTH / 3), fill='x', pady=30
	)
	
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
