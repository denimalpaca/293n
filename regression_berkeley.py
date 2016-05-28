import csv
import sys
from datetime import datetime
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor
import numpy
numpy.set_printoptions(threshold=numpy.nan)

data = []
target = []

num_comments_max = 0
score_max = 0
title_max = 0
gilded_max = 0

# Domain Categories
school_list = {"alumni.berkeley.edu", "blogs.berkeley.edu", "cs.berkeley.edu", "dailycal.org", "eecs.berkeley.edu", "engineering.berkeley.edu", "forage.berkeley.edu", "journalism.berkeley.edu", "news.berkeley.edu", "ocf.berkeley.edu", "police.berkeley.edu"}
local_list = {"bart.gov", "berkeleybeet.com", "berkeleydailyplanet.com", "berkeleyside.com", "blog.sfgate.com", "californiagoldenblogs.com", "calnature.org", "contracostatimes.com", "eastbayexpress.com", "insidebayarea.com", "mercurynews.com", "sanfrancisco.cbslocal.com", "sfchronicle.com", "sfgate.com"}
news_list = {"arstechnica.com", "baltimoresun.com", "abc7news.com", "blogs.wsj.com", "bloomberg.com", "espn.go.com", "forbes.com", "fortune.com", "geekwire.com", "huffingtonpost.com", "latimes.com", "npr.org", "nytimes.com", "reuters.com", "washingtonpost.com", "usatoday.com", "theatlantic.com", "theguardian.com"}
image_list = {"i.imgur.com", "imgur.com"}
video_list = {"youtu.be", "youtube.com", "vimeo.com"}
social_list = {"facebook.com", "m.facebook.com", "mobile.twitter.com", "reddit.com", "twitter.com"}

ifile = open(sys.argv[1], 'rb')

reader = csv.reader(ifile)

reader.next()
for row in reader:
	created_utc_raw = row[0]
	subreddit_raw = row[1]
	author_raw = row[2]
	domain_raw = row[3]
	url_raw = row[4]
	num_comments_raw = row[5]
	score_raw = row[6]
	ups_raw = row[7]
	downs_raw = row[8]
	title_raw = row[9]
	selftext_raw = row[10]
	gilded_raw = row[11]
	over_18_raw = row[12]
	thumbnail_raw = row[13]
	subreddit_id_raw = row[14]
	author_flair_css_class_raw = row[15]
	is_self_raw = row[16]
	author_flair_text_raw = row[17]

	created_utc = datetime.fromtimestamp(float(created_utc_raw))
	created_hour = created_utc.hour

	title_length = len(title_raw)
	# 1 is short, 2 is medium, 3 is long
	# TODO: Change these to appropriate values
	# Right now inputting raw length so this isn't used.
	if title_length <= 10:
		title = 1
	elif title_length > 10 and title_length <= 25:
		title = 2
	else:
		title = 3

	selftext_length = len(selftext_raw)
	# 1 is short, 2 is medium, 3 is long
	# TODO: Change these to appropriate values
	# Right now inputting raw length so this isn't used.
	if selftext_length <= 10:
		selftext = 1
	elif selftext_length > 10 and selftext_length <= 25:
		selftext = 2
	else:
		selftext = 3

	author_flair_text_length = len(author_flair_text_raw)
	if author_flair_text_length == 0:
		author_flair_text = 0
	else:
		author_flair_text = 1


	school = 0
	local = 0
	news = 0
	image = 0
	video = 0
	social = 0
	self = 0
	other = 0

	if is_self_raw == "true":
		self = 1
	elif domain_raw in local_list:
		local = 1
	elif domain_raw in news_list:
		news = 1
	elif domain_raw in image_list:
		image = 1
	elif domain_raw in video_list:
		video = 1
	elif domain_raw in social_list:
		social = 1
	elif "berkeley.edu" in domain_raw or domain_raw in school_list:
		school = 1
	else:
		other = 1

	in_sample = []
	in_sample.append(int(created_hour))
	in_sample.append(int(num_comments_raw))
	in_sample.append(int(title_length))
#	out_row.append(selftext_length)
#	in_sample.append(gilded_raw)
	in_sample.append(int(author_flair_text))
	in_sample.append(int(school))
	in_sample.append(int(local))
	in_sample.append(int(news))
	in_sample.append(int(image))
	in_sample.append(int(video))
	in_sample.append(int(social))
	in_sample.append(int(self))
	in_sample.append(int(other))

	data.append(in_sample)
	target.append(int(score_raw))

ifile.close()

#clf = RandomForestRegressor()
#clf.fit(data[:600], target[:600])
#score = clf.score(data[600:], target[600:])
#print score
#print clf.feature_importances_

clf = svm.SVR()
clf.fit(data[:600], target[:600])
score = clf.score(data[600:], target[600:])
print score




