from linkhome.tests import *

class TestProcfsController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='procfs'))
        # Test response...
