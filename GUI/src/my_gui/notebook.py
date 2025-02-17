from tkinter.ttk import Notebook, Frame
from tkinter import PhotoImage
from os import path


ICONS_DIR = path.abspath(path.join(path.dirname(__file__), path.pardir, path.pardir, 'icons'))


class Tab:
	def __init__(self, parent: Notebook, title: str, image_png: str):
		self.frame = Frame(parent)
		self.__notebook = parent
		self.__icon = PhotoImage(file=path.join(ICONS_DIR, image_png))
		parent.add(self.frame, text=title, image=self.__icon, compound='left')

	def show(self):
		self.__notebook.select(self.frame)  # Correct way to show the tab

	def hide(self):
		tab_id = self.__notebook.index(self.frame)
		self.__notebook.hide(tab_id)
		return self
