import sublime, sublime_plugin, os, json, re
from os.path import basename

class pathInfo:
	def __init__(self, path):
		self.path = path
		self.project_path = os.path.dirname(self.path)
		self.project_name = self.project_path.split("/")[-1]
		self.framer_path = self.project_path+"/framer"
		self.view_file = self.framer_path+"/views."+self.project_name+".js"
	
class FramerCompletion(sublime_plugin.EventListener):
	settings = sublime.load_settings('FramerCompletion.sublime-settings')

	docCompletions, completions = [], [] # empty lists to save completions in

	# Add Framer docs
	pluginFolder = os.path.dirname(os.path.abspath(__file__))
	with open(os.path.join(pluginFolder,"framerdocs.json")) as json_file: #add this to class?
		json_data = json.load(json_file)
		for key in json_data:
			docCompletions.append((key,json_data[key]))

	def is_supported_file(self, filePath):
		if filePath is not None: # only run on saved files
			if os.path.isdir(pathInfo(filePath).framer_path):
				fileExtension = os.path.splitext(filePath)[1]
				if fileExtension == ".js" or ".html":
					return True

	def findViews(self, filePath):
		viewfile = pathInfo(filePath).view_file
		with open(viewfile) as file_lines:
			dotNotation = self.settings.get('dotNotation')
			self.completions[:] = [] # clear to refresh list
			for line in file_lines:
				if "name" in line:
					pattern = r'"([^"]*)"' # inside quotes
					viewname = re.findall(pattern, line)[1]	
					if dotNotation:
						view = "PSD."+viewname
					else:
						view = "PSD[\""+viewname+"\"]"
					self.completions.append((view+'\t'+"Framer",view)) #append a tuple with text to display and insert
			self.completions.sort() # alphabetical order

	def on_activated(self, view):
		if self.is_supported_file(view.file_name()):
			self.findViews(view.file_name())

	def on_query_completions(self, view, prefix, locations):
		if self.is_supported_file(view.file_name()):
			return self.completions + self.docCompletions