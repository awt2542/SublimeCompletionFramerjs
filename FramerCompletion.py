import sublime, sublime_plugin, os, json, re
from os.path import basename

class PathInfo:
	def __init__(self, path):
		self.path = path
		self.project_path = os.path.dirname(self.path)
		self.project_name = self.project_path.split("/")[-1]
		self.framer_path = self.project_path+"/framer"
		self.view_file = self.framer_path+"/views."+self.project_name+".js"
		self.framer_file = self.framer_path+"/framer.js"

class FramerCompletion(sublime_plugin.EventListener):
	settings = sublime.load_settings('FramerCompletion.sublime-settings')
	js_2docs, coffee_2docs, js_3docs, coffee_3docs, completions = [], [], [], [], []

	# Add Framer docs
	plugin_dir = os.path.dirname(os.path.abspath(__file__))
	with open(plugin_dir+"/framer2docs-js.json") as json_file:
		json_data = json.load(json_file)
		for key in json_data:
			js_2docs.append((key.encode('utf-8')+'\t'+"Framer",json_data[key]))
	with open(plugin_dir+"/framer2docs-coffee.json") as json_file:
		json_data = json.load(json_file)
		for key in json_data:
			coffee_2docs.append((key.encode('utf-8')+'\t'+"Framer",json_data[key]))
	with open(plugin_dir+"/framer3docs-js.json") as json_file:
		json_data = json.load(json_file)
		for key in json_data:
			js_3docs.append((key.encode('utf-8')+'\t'+"Framer",json_data[key]))
	with open(plugin_dir+"/framer3docs-coffee.json") as json_file:
		json_data = json.load(json_file)
		for key in json_data:
			coffee_3docs.append((key.encode('utf-8')+'\t'+"Framer",json_data[key]))
	

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
		with open(PathInfo(view.file_name()).framer_file) as f:
			
			if re.search(r'Framer 2',f.readline()) is not None:
				#framer 2 project
				if view.match_selector(locations[0], "source.js, source.js.embedded.html"):
					if self.is_supported_file(view.file_name()):
						return self.completions + self.js_2docs
				elif view.match_selector(locations[0], "source.coffee"):
					if self.is_supported_file(view.file_name()):
						return self.completions + self.coffee_2docs
			else:
				#probably a framer 3 project
				if view.match_selector(locations[0], "source.js, source.js.embedded.html"):
					if self.is_supported_file(view.file_name()):
						return self.completions + self.js_3docs
				elif view.match_selector(locations[0], "source.coffee"):
					if self.is_supported_file(view.file_name()):
						return self.completions + self.coffee_3docs