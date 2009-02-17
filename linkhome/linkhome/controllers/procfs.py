import logging
import os


from linkhome.lib.base import *

log = logging.getLogger(__name__)

class ProcfsController(BaseController):
    
    def index(self):
        paths = filter(lambda p: os.path.isfile(os.path.join('/proc', p)),
                       os.listdir('/proc'))
        paths.sort()
        return render('/procfs/index.mako', files = paths)

    def get(self, id):
        fname = os.path.join('/proc', id)
        f = open(fname, 'r')
        text = f.read()
        f.close()
        return render('/procfs/file.mako', filename = fname, contents = text)
            
