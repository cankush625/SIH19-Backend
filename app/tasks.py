import requests
from app.models import Website
import time
from app import db

def getStatus(url):
	try:
		r = requests.get(url)
	except:
		r = requests.get('https://google.com') 
	return r.status_code


def websiteCheck():
	while True:
		websites = Website.query.all()
		for website in websites:
			print(f"Checking {website.name}")
			website.http_status_code = getStatus(website.url)
			time.sleep(2)
		db.session.commit()

