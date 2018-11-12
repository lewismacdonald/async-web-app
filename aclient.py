import asyncio
import aiohttp
import requests

import variants

import datetime

class Client:

	@variants.primary
	def get_url(self, url):
		print("Sent Request for %s" % url)
		return requests.get(url).content

	@get_url.variant('async')
	async def get_url(self, url):
		try:
			async with aiohttp.request('GET', url) as response:
				print("Sent Request for %s" % url)
				return await response.content.read()
		except:
			return ""



def async_url_length(urls, event_loop):
	client = Client()
	responses = event_loop.run_until_complete(
		asyncio.gather(
			*[client.get_url.async(x) for x in urls]
		)
	)
	return list(map(len, responses))

if __name__=='__main__':
	urls = [
	"https://github.com",
	"https://facebook.com",
	"https://google.com",
	"https://ebay.com",
	"https://amazon.co.uk",
	"https://twitter.com",
	"https://docs.python.org/3.3/library/functions.html#open"
	]


	urls = urls*10

	total = len(urls)
	
	client = Client()
	loop = asyncio.get_event_loop()
	r = async_url_length(urls, loop)
	start = datetime.datetime.now()
	async_items = loop.run_until_complete(
		asyncio.gather(
			*[client.get_url.async(x) for x in urls]
		)
	)
	print(list(map(len, async_items)))
	mid = datetime.datetime.now()

	print("async time taken for %s urls:" % total, mid-start)
	sync_items = [
		client.get_url(x)
		for x in urls
	]
	end = datetime.datetime.now()
	print(list(map(len, sync_items)))
	print("sync time taken for %s urls:" % total, end-mid)

	for i, c in enumerate(sync_items):
		file = f"{str(i)}_sync.txt"
		with open(file, 'wb') as f:
			f.write(c)

	for i, c in enumerate(async_items):
		file = f"{str(i)}_async.txt"
		with open(file, 'wb') as f:
			f.write(c)