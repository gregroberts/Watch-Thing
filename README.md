#Watch Thing

##For watching things.

Interface for when you wanna watch something but can't decide. 

##Usage
###From the Command Line

	>python watch_thing.py <method> <*args>

Method can be either 'show' or 'site'

if 'show' args needed are show
name, from shows.json.

if 'site' args needed are site name (from sites.json) and name of show to watch.

e.g.

	C:\Users\Gerg\Documents\GitHub\Watch-Thing>python watch_thing.py simpsons
	now watching simpsons

	C:\Users\Gerg\Documents\GitHub\Watch-Thing>

or,

	C:\Users\Gerg\Documents\GitHub\Watch-Thing>python watch_thing.py site putlocker frasier
	now watching putlocker
	now watching frasier

	C:\Users\Gerg\Documents\GitHub\Watch-Thing>

and each time, a browser should open up.


###From the REPL

	C:\Users\Gerg\Documents\GitHub\Watch-Thing>python
	Python 2.7.5 |Anaconda 1.8.0 (32-bit)| (default, Jul  1 2013, 12:41:55) [MSC v.1500 32 bit (Intel)] on win32
	Type "help", "copyright", "credits" or "license" for more information.
	>>> from watch_thing import *

####Create a Show or Site instance using one of the names in the json files, 

	>>> show = get_show('simpsons')
	now watching simpsons
	>>> show.go()

####or roll your own:

	>>> show = Episoder(name = 'south park',
						url = 'http://www.watchseries.li/episode/south_park_s%d_e%d.html',
						seasons = [1,19],
						eps = [1,15])
	now watching south park
	>>> show.go()
	>>> show.save()

####Or do the same thing on a site level

	>>> site = get_site('putlocker')
	now watching putlocker
	>>> site.set_show('brooklyn-nine-nine')
	now watching brooklyn-nine-nine
	>>> site.go()
	>>> site.set_show('adventure-time')
	now watching adventure-time
	>>> site.go()
	>>>

####and add new sites

	>>> site = Site(name = 'watchseries.li',
					url = 'http://watchseries.li/episode/%s_s%%d_e%%d.html')
	now watching watchseries.li
	>>> site.set_show('futurama')
	now watching futurama
	>>> site.go()
	>>> site.save()


##Does it do any neat tricks?

Sort of. If you choose a show but haven't set the seasons, eps argument, it will guess seasons and episodes, and reduce the range it guesses in until it finds a working link. Future calls will be between those bounds.


It also saves your history in a csv. When you go to choose an episode, it checks your history and then chooses an episode you haven't seen.


Contributers welcome.

TODO:
Add non-random functionality
Add database backends
Turn into API service

