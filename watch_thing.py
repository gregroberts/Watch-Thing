from random import randint
import webbrowser
import time
import csv
import requests 
import json
from sys import argv

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
		print 'now watching %s' % name
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
				print '''looking for eps (%d,%d),(%d,%d)
				''' % (tuple(self.eps + self.seasons))
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

	def save(self):
		obj = {
			'name': self.name,
			'url': self.url
		}
		with open(sites_json, 'rb') as f:
			sites = json.load(f)
		sites.append(obj)
		with open(sites_json, 'wb') as f:
			json.dump(sites, f)


class Site(Episoder):
	orig_url = ''
	def reset_choices(self):
		seasons, eps = [1, 100], [1, 100]

	def set_show(self, show):
		print 'now watching %s' % show
		if self.orig_url == '':
			self.orig_url = self.url
		self.url = self.orig_url % show
		self.name = show
		self.reset_choices()

	def save(self):
		obj = {
			'name': self.name,
			'url': self.url,
			'seasons': self.seasons,
			'eps': self.eps
		}
		with open(shows_json, 'rb') as f:
			shows = json.load(f)
		shows.append(obj)
		with open(shows_json, 'wb') as f:
			json.dump(shows, f)



def get_json(floc):
	try:
		with open(floc, 'rb') as f:
			json_data = json.load(f)
		return json_data
	except Exception as e:
		print 'failed to open %s with Exception %s' % (floc,e)
		return []	

shows_json = 'shows.json'
sites_json = 'sites.json'

def auto_show(args):
	show = Episoder(**args)
	show.go()
	return show

default = 'simpsons'

def get_show(show):
		res = filter(lambda x: x['name'] == show, get_json(shows_json))
		if len(res) == 1:
			return auto_show(res[0])
		elif len(res) > 1:
			print '%d results found:\n ' % len(results)
			print '\n'.join(map(lambda x: x['name'], res))
			return res
		else:
			print 'no such show as %s' % show		

def get_site(site):
		res = filter(lambda x: site in x['name'], get_json(sites_json))
		if len(res) == 1:
			return Site(**res[0])
		if len(res) > 1:
			print '%d results found:\n ' % len(results)
			print '\n'.join(map(lambda x: x['name'], res))
			return res
		else:
			print 'no such site as %s' % site		

def cli(*args):
	if args[0] == 'show':
		show = args[1]
		get_show(show)
	if args[0] == 'site':
		site = get_site(args[1])
		if site and type(site) is not list:
			site.set_show(args[2])
			site.go()
	else:
		get_show(default)






if __name__ == '__main__':
	cli(*argv[1:])