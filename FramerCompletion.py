import sublime, sublime_plugin, os, json
from os.path import basename

class FramerCompletionCommand(sublime_plugin.EventListener):

	docCompletions = [] # list to save doc completion tuples in
	completions = [] # list to save completion tuples in

	dirkname, file2name = os.path.split(os.path.abspath(__file__))
	os.chdir(dirkname)
	json_file = open("framerdocs.json")
	try:
		json_data = json.load(json_file)
		for key in json_data:
			docCompletions.append((key,json_data[key]))
	except Exception, e:
		print e
	else:
		json_file.close()
	

	def findViews(self, path):
		try:
			file_lines = open(path)
			for line in file_lines:
				if "name" in line:
					line = line.strip().strip('"name": "').strip('",') # ugly clean up of string
					view = "PSD[\""+line+"\"]"
					self.completions[:] = [] # clear the list to refresh
					self.completions.append((view+'\t'+"Framer",view)) #append a tuple with text to display and insert
			self.completions.sort() # make results show in alphabetical order
		except IOError:
			print "input error views"
		else:
			file_lines.close()

	def on_activated(self, view):
		pathToFile = os.path.dirname(view.file_name()) # path to this file
		projectName = pathToFile.split("/")[-1]
		fileName = view.file_name().split("/")[-1]
		viewsPath = pathToFile+"/framer/views."+projectName+".js"
		if ".js" in fileName:
			os.chdir(pathToFile)
			self.findViews(viewsPath)
		else:
			self.completions[:] = [] # clear the list

	def on_query_completions(self, view, prefix, locations):
		return self.completions + self.docCompletions