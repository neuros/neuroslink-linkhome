import logging
import os
import subprocess

from linkhome.lib.base import *

log = logging.getLogger(__name__)

class ApplicationsController(BaseController):
    
    def index(self):
        paths = filter(lambda p: os.path.isfile(os.path.join('/usr/share/applications', p)),
                       os.listdir('/usr/share/applications'))
        paths.sort()
        return render('/applications/index.mako', files = paths)

    def get(self, id):
        fname = os.path.join('/usr/share/applications', id)
        f = open(fname, 'r')
        
	command = "Unknown"
	
	# come up with some better parsing for this section
	for line in f:
		if line.startswith("Exec="):
			command = line.partition("=")
	f.close()

	f = open('/dev/null','w')

	# 
	subprocess.Popen([command[2].strip()],stdout=f,stderr=f)

        return render('/applications/launched.mako', filename = fname, contents = command[2].strip() )
            
