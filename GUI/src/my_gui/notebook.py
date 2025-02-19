from tkinter.ttk import Notebook, Frame
from tkinter import PhotoImage
from os import path
import sys


def get_resource_path(relative_path):
	if getattr(sys, 'frozen', False):
		base_path = sys._MEIPASS
	else:
		base_path = path.abspath(".")
	return path.join(base_path, relative_path)


DIR_ICONS = get_resource_path('icons')


class Tab:
	def __init__(self, parent: Notebook, title: str, image_png: str):
		self.frame = Frame(parent)
		self.__notebook = parent
		self.__icon = PhotoImage(file=path.join(DIR_ICONS, image_png))
		parent.add(self.frame, text=title, image=self.__icon, compound='left')

	def show(self):
		self.__notebook.select(self.frame)  # Correct way to show the tab

	def hide(self):
		tab_id = self.__notebook.index(self.frame)
		self.__notebook.hide(tab_id)
		return self
