import logging
import os
import subprocess
import mimetypes

class DesktopEntry:
	def Import(self, path, name):
		self.name = name.partition(".")[0].strip()
		self.fname = name.strip()
		self.fullpath = os.path.join(path,name).strip()
		self.Comment = "No Information.."
		self.Icon = "/applications/icons/default-icon.png"

	        f = open(os.path.join(path,name), 'r')
		for line in f:
                	if line.startswith("Exec="):
                        	self.Exec = line.partition("=")[2].strip()
			if line.startswith("Name="):
				self.AppName = line.partition("=")[2].strip()

			if line.startswith("Comment="):
				self.Comment = line.partition("=")[2].strip()

			if line.startswith("Icon="):
				self.Icon = line.partition("=")[2].strip()
		f.close()		

from linkhome.lib.base import *

log = logging.getLogger(__name__)

class ApplicationsController(BaseController):
    
	def index(self):
		paths = filter(lambda p: os.path.isfile(os.path.join('/usr/share/linkhome', p)),
		                       os.listdir('/usr/share/linkhome'))
		paths.sort()

		list = []
		for file in paths:
			entry = DesktopEntry()
			entry.Import('/usr/share/linkhome',file)
			list.append(entry)

		return render('/applications/index.mako', files = list)

	def get(self, id):
		entry = DesktopEntry()
		entry.Import('/usr/share/linkhome',id.strip() + '.desktop')

		# Open the process and start it in subprocess.
		# This will be replaced by d-bus application launcher because
		# if web daemon closes then so does the application.

		try:
			f = open('/dev/null','w')
			subprocess.Popen([entry.Exec],stdout=f,stderr=f)
		except:
			return render('/applications/error.mako', error = entry)

		return render('/applications/launched.mako', application = entry)
            

	def properties(self, app, prop):
		entry = DesktopEntry()
		entry.Import('/usr/share/linkhome',app.strip() + '.desktop')
		print 'Running Properties '  + app + " " + prop
		print 'File Name: ' + entry.fname

		if prop.strip() == 'icon':
			print "Found The Icon! "
			f = open(entry.Icon,'r')
			data = f.read()
			f.close
			response.headers['Content-type'] = mimetypes.guess_type(entry.Icon)
			return data

		elif prop.strip() == 'launch':
			print "Launch is run! " + prop.strip() + " " + prop
			try:
				f = open('/dev/null','w')
				subprocess.Popen([entry.Exec],stdout=f,stderr=f)
			except:
				return render('/applications/error.mako', error = entry)

			return render('/applications/launched.mako', application = entry)
		elif prop.strip() == 'info':

			return render('/application/launched.mako', application = entry)

