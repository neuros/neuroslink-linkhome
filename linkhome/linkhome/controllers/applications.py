import logging
import os
import subprocess


class DesktopEntry:

	def Import(self, path, name):
		self.fname = name.strip()
		self.fullpath = os.path.join(path,name).strip()
		self.Comment = "No Information.."

	        f = open(os.path.join(path,name), 'r')
		for line in f:
                	if line.startswith("Exec="):
                        	self.Exec = line.partition("=")[2].strip()

			if line.startswith("Name="):
				self.AppName = line.partition("=")[2].strip()

			if line.startswith("Comment="):
				self.Comment = line.partition("=")[2].strip()
	        f.close()		
		

from linkhome.lib.base import *

log = logging.getLogger(__name__)

class ApplicationsController(BaseController):
    
    def index(self):
        paths = filter(lambda p: os.path.isfile(os.path.join('/usr/share/applications', p)),
                       os.listdir('/usr/share/applications'))
        paths.sort()

	list = []
	for file in paths:
		entry = DesktopEntry()
		entry.Import('/usr/share/applications',file)
		list.append(entry)

        return render('/applications/index.mako', files = list)

    def get(self, id):
	entry = DesktopEntry()
	entry.Import('/usr/share/applications',id)

	# Open the process and start it in subprocess.
	# This will be replaced by d-bus application launcher because
	# if web daemon closes then so does the application.

	try:
		f = open('/dev/null','w')
		subprocess.Popen([entry.Exec],stdout=f,stderr=f)
	except:
		return render('/applications/error.mako', error = entry)

        return render('/applications/launched.mako', application = entry)
            

