import sublime, sublime_plugin, os, json
from os.path import basename

class FramerCompletionCommand(sublime_plugin.EventListener):

	completions = [] # list to save completion tuples in

	def addDocs(self):
		json_file = open("framerdocs.json")
		json_data = json.load(json_file)
		for key in json_data:
			self.completions.append((key,json_data[key]))

	def findViews(self, path):
		try:
			file_lines = open(path)
			for line in file_lines:
				if "name" in line:
					line = line.strip().strip('"name": "').strip('",') # ugly clean up of string
					view = "PSD[\""+line+"\"]"
					self.completions.append((view+'\t'+"Framer",view)) #append a tuple with text to display and insert
			self.completions.sort() # make results show in alphabetical order
		except IOError:
			pass # file wasn't found/couldn't open
		else:
			file_lines.close()

	def on_activated(self, view):
		pathToFile = os.path.dirname(view.file_name()) # path to this file
		projectName = pathToFile.split("/")[-1]
		fileName = view.file_name().split("/")[-1]
		viewsPath = pathToFile+"/framer/views."+projectName+".js"
		if ".js" in fileName:
			self.completions[:] = [] # clear the list to refresh
			self.addDocs()
			self.findViews(viewsPath)
		else:
			self.completions[:] = [] # clear the list

	def on_query_completions(self, view, prefix, locations):
		return self.completions