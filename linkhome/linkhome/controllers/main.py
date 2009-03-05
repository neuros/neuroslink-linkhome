import logging
import os

from linkhome.lib.base import *

log = logging.getLogger(__name__)


class MainController(BaseController):
    
	def index(self):
		return render('/main/index.mako')
