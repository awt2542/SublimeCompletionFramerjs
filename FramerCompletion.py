import sublime, sublime_plugin, os, json, re
from os.path import basename

class FramerCompletionCommand(sublime_plugin.EventListener):

	def is_supported_format(self, view):
		if ".js" in view.file_name() or ".html" in view.file_name():
			return True

	docCompletions = [] # list to save doc completion tuples in
	completions = [] # list to save completion tuples in

	dirname = os.path.dirname(os.path.abspath(__file__))
	json_file = open(os.path.join(dirname,"framerdocs.json"))
	try:
		json_data = json.load(json_file)
		for key in json_data:
			docCompletions.append((key,json_data[key]))
	except Exception, e:
		pass
	else:
		json_file.close()

	def findViews(self, path):
		try:
			file_lines = open(path)
			self.completions[:] = [] # clear the list to refresh
			for line in file_lines:
				if "name" in line:
					pattern = r'"([^"]*)"' # inside quotes
					viewname = re.findall(pattern, line)[1]	
					view = "PSD[\""+viewname+"\"]"
					self.completions.append((view+'\t'+"Framer",view)) #append a tuple with text to display and insert
			self.completions.sort() # alphabetical order
		except Exception, e:
			pass
		else:
			file_lines.close()

	def on_activated(self, view):
		if view.file_name() is not None: # only run on saved files
			pathToFile = os.path.dirname(view.file_name())
			if os.path.exists(os.path.join(pathToFile,"framer/framer.js")): # a framer project
				projectName = pathToFile.split("/")[-1]
				viewsPath = pathToFile+"/framer/views."+projectName+".js"
				if self.is_supported_format(view):
					self.findViews(viewsPath)
		

	def on_query_completions(self, view, prefix, locations):
		if self.is_supported_format(view):
			return self.completions + self.docCompletions