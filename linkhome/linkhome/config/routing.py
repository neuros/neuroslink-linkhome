"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('error/:action/:id', controller='error')
    
    map.connect('/proc', controller='procfs', action='index')
    map.connect('/proc/:id', controller='procfs', action='get')

    map.connect('/applications', controller='applications', action='index')
    map.connect('/applications/:id', controller='applications', action='get')

    map.connect(':controller/:action/:id')
    map.connect('*url', controller='template', action='view')

    return map
