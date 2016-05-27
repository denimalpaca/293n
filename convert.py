import csv
from datetime import datetime

# Domain Categories
school_list = {"alumni.berkeley.edu", "blogs.berkeley.edu", "cs.berkeley.edu", "dailycal.org", "eecs.berkeley.edu", "engineering.berkeley.edu", "forage.berkeley.edu", "journalism.berkeley.edu", "news.berkeley.edu", "ocf.berkeley.edu", "police.berkeley.edu"}
local_list = {"bart.gov", "berkeleybeet.com", "berkeleydailyplanet.com", "berkeleyside.com", "blog.sfgate.com", "californiagoldenblogs.com", "calnature.org", "contracostatimes.com", "eastbayexpress.com", "insidebayarea.com", "mercurynews.com", "sanfrancisco.cbslocal.com", "sfchronicle.com", "sfgate.com"}
news_list = {"arstechnica.com", "baltimoresun.com", "abc7news.com", "blogs.wsj.com", "bloomberg.com", "espn.go.com", "forbes.com", "fortune.com", "geekwire.com", "huffingtonpost.com", "latimes.com", "npr.org", "nytimes.com", "reuters.com", "washingtonpost.com", "usatoday.com", "theatlantic.com", "theguardian.com"}
image_list = {"i.imgur.com", "imgur.com"}
video_list = {"youtu.be", "youtube.com", "vimeo.com"}
social_list = {"facebook.com", "m.facebook.com", "mobile.twitter.com", "reddit.com", "twitter.com"}

in_file_name = raw_input("Enter file name (.csv): ")
out_file_name = in_file_name[:-4]+"_out.csv"

ifile = open(in_file_name, 'rb')
ofile = open(out_file_name, 'wb')

reader = csv.reader(ifile)
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

label = ["created_hour","subreddit","author","num_comments","score","title","selftext","gilded","author_flair_text","is_school","is_local","is_news","is_image","is_video","is_social","is_self","is_other"]
writer.writerow(label)

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

	out_row = []
	out_row.append(created_hour)
	out_row.append(subreddit_raw)
	out_row.append(author_raw)
	out_row.append(num_comments_raw)
	out_row.append(score_raw)
	out_row.append(title_length)
	out_row.append(selftext_length)
	out_row.append(gilded_raw)
	out_row.append(author_flair_text)
	out_row.append(school)
	out_row.append(local)
	out_row.append(news)
	out_row.append(image)
	out_row.append(video)
	out_row.append(social)
	out_row.append(self)
	out_row.append(other)
	writer.writerow(out_row)
ifile.close()
ofile.close()

