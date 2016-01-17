from random import randint
import webbrowser
import mechanize
import time
import csv
import requests 

class Episoder:
	history = [[0,0]]
	season, ep = 0,0
	name, url = 'Episoder', ''
	seasons, eps = [1, 20], [1, 20]
	guess = True

	def _get_history():
		try:
			with open('EPISODESMEM.csv', 'rb') as f:
				w = csv.reader(f)
				rows = [i for i in w]
				returnfilter(lambda x: x[0] == self.name, rows)
		except:
			print 'no history :('
	
	def _set_history(self, season, ep):
		with open('EPISODESMEM.csv', 'ab+') as f:
			w = csv.writer(f)
			w.writerow([self.name, season, ep])

	def _get_url(self, season, ep):
		url = self.url % (season,ep)
		return url
	
	def __init__(self, name, url, seasons = [], eps = []):
		self.name = name
		self.url = url
		if seasons == []:
			self.guess = False
		else:
			self.seasons, self.eps = seasons, eps
	
	def get(self, season , ep):
		webbrowser.open(self._get_url(season, ep))

	def attempt(self, season, ep):
		req = requests.get(self._get_url(season, ep))
		return req.ok

	def gen(self, guess):
		rn = lambda a, b: randint(a, b)
		season, ep = rn(*self.seasons), rn(*self.eps)			
		if guess == False:
			guess = self.attempt(season, ep)
			if self.eps[1] > 1:
				self.eps[1] = self.eps[1] - 1
			else:
				self.eps[1] = 20
				print 'looking for eps'
				self.seasons[1] = self.seasons[1] - 1	
		self._set_history(season, ep)
		return season, ep, guess

	def choose(self):
		rn = lambda a, b: randint(a, b)
		guess = self.guess
		season, ep = rn(*self.seasons), rn(*self.eps)	
		while [season, ep] in self.history or guess == False:
			season, ep, guess = self.gen(guess)
		return season, ep

	def go(self):
		sep = self.choose()
		self.get(*sep)


class Site(Episoder):
	orig_url = ''

	def reset_choices(self):
		seasons, eps = [1, 100], [1, 100]

	def set_show(self, show):
		if self.orig_url == '':
			self.orig_url = self.url
		self.url = self.orig_url % show
		self.name = show
		self.reset_choices()





shows = [
	{
	"url": "http://putlocker.is/watch-the-simpsons-tvshow-season-%d-episode-%d-online-free-putlocker.html",
	"name":"simpsons",
	"choices" : [(11,25),(1,15)]
	}
]

sites = [
	{
	 'name':'putlocker',
	 'url': 'http://putlocker.is/watch-%s-tvshow-season-%%d-episode-%%d-online-free-putlocker.html'
	}
]



def auto_show(args):
	show = Episoder(**args)
	show.go()

def get_show(show):
		res = filter(lambda x: x['name'] == show, shows)
		if len(res) == 1:
			auto_go(res[0])
		if len(res) > 2:
			print '%d results found:\n ' % len(results)
			print '\n'.join(map(lambda x: x['name'], res))
		else:
			print 'no such show as %s' % show		

def get_site(site):
		res = filter(lambda x: x['name'] == site, sites)
		if len(res) == 1:
			return Site(**res[0])
		if len(res) > 2:
			print '%d results found:\n ' % len(results)
			print '\n'.join(map(lambda x: x['name'], res))
			return res
		else:
			print 'no such site as %s' % site		

def cli(method, *args):
	if method == 'show':
		if len(args) == 1:
			show = args[0]
			get_show(show)
		if len(args) > 1:
			auto_show(*args)
		else:
			get_show(default)



default = 'simpsons'




if __name__ == '__main__':
	#gg = Site('putlocker', 'http://putlocker.is/watch-%s-tvshow-season-%%d-episode-%%d-online-free-putlocker.html')
	#gg.set_show('frasier')
	#gg.go()
	cli()
	#gg = get_site('putlocker')
	#gg.set_show('frasier')
	#gg.go() 
