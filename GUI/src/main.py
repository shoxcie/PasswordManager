import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from string import punctuation
import pyperclip
import os

import my_gui


#-----------#
# Constants #
#-----------#
WIN_TITLE = "Password Manager"
WIN_MIN_WIDTH, WIN_MIN_HEIGHT = 700, 580
WIN_WIDTH, WIN_HEIGHT = 700, 580

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
	
	tab_file_frame = ttk.Frame(tab_file.frame)
	tab_file_frame.pack(fill='x', expand=True)
	
	ttk.Button(tab_file_frame, text="Select", command=tab_file_onclick_select).pack(
		padx=(WIN_MIN_WIDTH / 3), fill='x'
	)
	
	ttk.Button(tab_file_frame, text="Create", command=tab_file_onclick_create).pack(
		padx=(WIN_MIN_WIDTH / 3), fill='x', pady=30
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
	
	tab_signup_frame = ttk.Frame(tab_signup.frame)
	tab_signup_frame.pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', expand=True
	)
	
	ttk.Button(tab_signup_frame, text="Toggle View", command=tab_signup_onclick_show).pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', pady=20
	)
	
	ttk.Label(tab_signup_frame, text="Password:").pack(anchor='w')
	tab_signup_entry = ttk.Entry(tab_signup_frame, show='*')
	tab_signup_entry.pack(fill='x')
	
	ttk.Label(tab_signup_frame, text="Repeat Password:").pack(anchor='w')
	tab_signup_entry_echo = ttk.Entry(tab_signup_frame, show='*')
	tab_signup_entry_echo.pack(fill='x')
	
	ttk.Button(tab_signup_frame, text="Confim", command=tab_signup_onclick_confirm).pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', pady=30
	)
	
	#------------#
	# Tab: Login #
	#------------#
	tab_login_show_bool = False
	
	def tab_login_onclick_show():
		nonlocal tab_login_show_bool
		tab_login_show_bool = not tab_login_show_bool
		
		if tab_login_show_bool:
			tab_login_entry.config(show='')
		else:
			tab_login_entry.config(show='*')
	
	def tab_login_onclick_confirm():
		pass
		# TODO: Decrypt the database file with tab_login_entry.get() password
		#	if the password is correct, hide the Login tab,
		#		then show Password, Database and Entry tabs
		#		and fill the Database tab's treeview
		#	else, show error message
	
	if not tab_file_reason:
		tab_login.show()
	
	tab_login_frame = ttk.Frame(tab_login.frame)
	tab_login_frame.pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', expand=True
	)
	
	ttk.Button(tab_login_frame, text="Toggle View", command=tab_login_onclick_show).pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', pady=20
	)
	
	ttk.Label(tab_login_frame, text="Password:").pack(anchor='w')
	tab_login_entry = ttk.Entry(tab_login_frame, show='*')
	tab_login_entry.pack(fill='x')
	
	ttk.Button(tab_login_frame, text="Confim", command=tab_login_onclick_confirm).pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', pady=30
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
	
	tab_password_frame = ttk.Frame(tab_password.frame)
	tab_password_frame.pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', expand=True
	)
	
	ttk.Button(tab_password_frame, text="Toggle View", command=tab_password_onclick_show).pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', pady=20
	)
	
	ttk.Label(tab_password_frame, text="Current Password:").pack(anchor='w')
	tab_password_entry = ttk.Entry(tab_password_frame, show='*')
	tab_password_entry.pack(fill='x')
	
	ttk.Label(tab_password_frame, text="New Password:").pack(anchor='w')
	tab_password_entry_new = ttk.Entry(tab_password_frame, show='*')
	tab_password_entry_new.pack(fill='x')

	ttk.Label(tab_password_frame, text="Repeat New Password:").pack(anchor='w')
	tab_password_entry_new_echo = ttk.Entry(tab_password_frame, show='*')
	tab_password_entry_new_echo.pack(fill='x')
	
	ttk.Button(tab_password_frame, text="Confim", command=tab_password_onclick_confirm).pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', pady=30
	)
	
	#---------------#
	# Tab: Database #
	#---------------#
	def tab_database_onclick_add():
		tab_entry_clear_entries()
		tab_entry.show()
	
	def tab_database_onclick_edit():
		selected_item = tab_database_treeview.selection()
		if selected_item:
			tab_entry_clear_entries()
			tab_entry.show()
			selected_title = tab_database_treeview.item(selected_item, 'text')
			tab_entry_entry_title.insert(0, selected_title)
			# TODO: Decrypt database, find entry by the selected_title, fill the Entry tab with the data
	
	def tab_database_onclick_delete():
		selected_item = tab_database_treeview.selection()
		if selected_item:
			print(tab_database_treeview.item(selected_item, 'text'))
			# TODO: Decrypt database, find entry by the selected item's text, delete the entry from the database
			tab_database_treeview.delete(selected_item)
	
	test_data = [ # TODO: Remove this
		"YouTube", "GitHub", "Gmail", "Google", "Yahoo",
		"Yandex", "Aliexpress", "Amazon", "Wikipedia", "Wookieepedia",
		"Something1", "Something2", "Something3", "Something4", "Something5"
	]
	
	def tab_database_treeview_search(event=None):
		query = tab_database_entry.get().lower()
		# filtered_data = [item for item in data if query in item.lower()]
		filtered_data = [item for item in test_data if item.lower().startswith(query)]
		for item in tab_database_treeview.get_children():
			tab_database_treeview.delete(item)
		for item in filtered_data:
			tab_database_treeview.insert('', 'end', text=item)
	
	tab_database_frame = ttk.Frame(tab_database.frame)
	tab_database_frame.pack(
		fill='both', expand=True
	)
	
	ttk.Label(tab_database_frame, text="Search:").pack(anchor='n')
	tab_database_entry = ttk.Entry(tab_database_frame)
	tab_database_entry.pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', pady=(0, 20)
	)
	tab_database_entry.bind('<KeyRelease>', tab_database_treeview_search)
	
	tab_database_treeview = ttk.Treeview(tab_database_frame, show='tree', height=0)
	tab_database_treeview.pack(side='left', fill='both', expand=True)
	
	tab_database_treeview_scrollbar = my_gui.scrollbar.AutoScrollbar(
		tab_database_frame, orient='vertical', command=tab_database_treeview.yview
	)
	tab_database_treeview.configure(
		yscrollcommand=tab_database_treeview_scrollbar.set
	)
	
	for item in test_data:
		tab_database_treeview.insert("", tk.END, text=item)
	
	tab_database_footer_frame = ttk.Frame(tab_database.frame)
	tab_database_footer_frame.pack(
		fill='x', side='bottom'
	)
	
	ttk.Button(tab_database_footer_frame, text="Add", command=tab_database_onclick_add).pack(
		fill='x', side='left', expand=True
	)
	
	ttk.Button(tab_database_footer_frame, text="Edit", command=tab_database_onclick_edit).pack(
		fill='x', side='left', expand=True, padx=3
	)
	
	ttk.Button(tab_database_footer_frame, text="Delete", command=tab_database_onclick_delete).pack(
		fill='x', side='left', expand=True
	)
	
	#------------#
	# Tab: Entry #
	#------------#
	def tab_entry_clear_entries():
		tab_entry_entry_title.delete(0, tk.END)
		tab_entry_entry_login.delete(0, tk.END)
		tab_entry_entry_password.delete(0, tk.END)
	
	tab_entry_show_bool = False
	
	def tab_entry_onclick_show():
		nonlocal tab_entry_show_bool
		tab_entry_show_bool = not tab_entry_show_bool
		
		if tab_entry_show_bool:
			tab_entry_entry_password.config(show='')
		else:
			tab_entry_entry_password.config(show='*')
	
	def tab_entry_onclick_copy():
		pyperclip.copy(tab_entry_entry_password.get())
	
	def tab_entry_onclick_save():
		pass
		# TODO: Decrypt the database, check if exists entry with
		#	`tab_entry_entry_title.get()` title exitst
		#	if it does exits, change its data and save it
		#	else save it as a new entry
	
	tab_entry_frame = ttk.Frame(tab_entry.frame)
	tab_entry_frame.pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', expand=True
	)
	
	ttk.Label(tab_entry_frame, text="Title:").pack(anchor='w')
	tab_entry_entry_title = ttk.Entry(tab_entry_frame)
	tab_entry_entry_title.pack(fill='x')
	
	ttk.Label(tab_entry_frame, text="Login:").pack(anchor='w')
	tab_entry_entry_login = ttk.Entry(tab_entry_frame)
	tab_entry_entry_login.pack(fill='x')
	
	ttk.Label(tab_entry_frame, text="Password:").pack(anchor='w')
	tab_entry_entry_password = ttk.Entry(tab_entry_frame, show='*')
	tab_entry_entry_password.pack(fill='x')
	
	ttk.Button(tab_entry_frame, text="Toggle View", command=tab_entry_onclick_show).pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x', pady=20
	)
	
	ttk.Button(tab_entry_frame, text="Copy Password", command=tab_entry_onclick_copy).pack(
		padx=(WIN_MIN_WIDTH / 6), fill='x'
	)
	
	ttk.Button(tab_entry.frame, text="Save", command=tab_entry_onclick_save).pack(
		fill='x', side='bottom'
	)
	
	#----------#
	# MainLoop #
	#----------#
	root.mainloop()


if __name__ == '__main__':
	app()
