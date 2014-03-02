import sublime, sublime_plugin, os, json, re
from os.path import basename

class FramerCompletionCommand(sublime_plugin.EventListener):

	docCompletions = [] # list to save doc completion tuples in
	completions = [] # list to save completion tuples in

	dirname = os.path.dirname(os.path.abspath(__file__))
	os.chdir(dirname)
	json_file = open("framerdocs.json")
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
		pathToFile = os.path.dirname(view.file_name()) # path to current file
		projectName = pathToFile.split("/")[-1]
		viewsPath = pathToFile+"/framer/views."+projectName+".js"
		if ".js" in view.file_name():
			os.chdir(pathToFile)
			self.findViews(viewsPath)
		else:
			self.completions[:] = [] # clear the list

	def on_query_completions(self, view, prefix, locations):
		if ".js" in view.file_name(): # needs to support embeds too
			return self.completions + self.docCompletions