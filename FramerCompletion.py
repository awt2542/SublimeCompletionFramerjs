import sublime, sublime_plugin, os, json, re
from os.path import basename

class PathInfo:
	def __init__(self, path):
		self.path = path
		self.project_path = os.path.dirname(self.path)
		self.project_name = self.project_path.split("/")[-1]
		self.framer_path = self.project_path+"/framer"
		self.view_file = self.framer_path+"/views."+self.project_name+".js"

class FramerCompletion(sublime_plugin.EventListener):
	settings = sublime.load_settings('FramerCompletion.sublime-settings')
	doc_completions, completions = [], [] # empty lists to save completions in

	# Add Framer docs
	plugin_dir = os.path.dirname(os.path.abspath(__file__))
	with open(plugin_dir+"/framerdocs.json") as json_file:
		json_data = json.load(json_file)
		for key in json_data:
			doc_completions.append((key.encode('utf-8')+'\t'+"Framer",json_data[key]))
	

	def is_supported_file(self, file_path):
		if file_path is not None: # only run on saved files
			if os.path.isdir(PathInfo(file_path).framer_path): # framer project?
				file_extension = os.path.splitext(file_path)[1]
				if file_extension == ".js" or ".html":
					return True

	def findViews(self, file_path):
		with open(PathInfo(file_path).view_file) as file_lines:
			dot_notation = self.settings.get('dotNotation')
			self.completions[:] = [] # clear to refresh list
			for line in file_lines:
				if "name" in line:
					pattern = r'"([^"]*)"' # inside quotes
					viewname = re.findall(pattern, line)[1]	
					if dot_notation:
						view = "PSD."+viewname
					else:
						view = "PSD[\""+viewname+"\"]"
					self.completions.append((view.encode('utf-8')+'\t'+"Framer view",view))
			self.completions.sort()

	def on_activated(self, view): #when user actives a document/tab
		if self.is_supported_file(view.file_name()):
			self.findViews(view.file_name())

	def on_query_completions(self, view, prefix, locations): #when user types
		if view.match_selector(locations[0], "source.js, source.js.embedded.html"):
			if self.is_supported_file(view.file_name()):
				return self.completions + self.doc_completions
		elif view.match_selector(locations[0], "source.coffee"):
			if self.is_supported_file(view.file_name()):
				return self.completions