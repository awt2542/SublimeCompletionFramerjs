import sublime, sublime_plugin, os, json, re
from os.path import basename

class FramerCompletionCommand(sublime_plugin.EventListener):
	settings = sublime.load_settings('FramerCompletion.sublime-settings')

	docCompletions, completions = [], [] # empty lists to save completions in

	def is_supported_format(self, fileName):
		if ".js" in fileName or ".html" in fileName:
			return True
	
	# Add Framer docs
	pluginFolder = os.path.dirname(os.path.abspath(__file__))
	with open(os.path.join(pluginFolder,"framerdocs.json")) as json_file:
		json_data = json.load(json_file)
		for key in json_data:
			docCompletions.append((key,json_data[key]))

	def findViews(self, viewfile):
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
		if view.file_name() is not None: # only run on saved files
			pathToFile = os.path.dirname(view.file_name())
			if os.path.exists(os.path.join(pathToFile,"framer/framer.js")): # a framer project
				projectName = pathToFile.split("/")[-1]
				viewfile = pathToFile+"/framer/views."+projectName+".js"
				if self.is_supported_format(view.file_name()):
					self.findViews(viewfile)

	def on_query_completions(self, view, prefix, locations):
		if self.is_supported_format(view.file_name()):
			return self.completions + self.docCompletions