import csv
from datetime import datetime

in_file_name = raw_input("Enter file name (.csv): ")
out_file_name = in_file_name[:-4]+"_out.csv"

ifile = open(in_file_name, 'rb')
ofile = open(out_file_name, 'wb')

reader = csv.reader(ifile)
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

label = ["created_hour","subreddit","author","num_comments","score","title","selftext","author_flair_text"]
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
	if title_length <= 10:
		title = 1
	elif title_length > 10 and title_length <= 25:
		title = 2
	else:
		title = 3

	selftext_length = len(selftext_raw)
	# 1 is short, 2 is medium, 3 is long
	# TODO: Change these to appropriate values
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

	out_row = []
	out_row.append(created_hour)
	out_row.append(subreddit_raw)
	out_row.append(author_raw)
	out_row.append(num_comments_raw)
	out_row.append(score_raw)
	out_row.append(title)
	out_row.append(selftext)
	out_row.append(author_flair_text)
	writer.writerow(out_row)
ifile.close()
ofile.close()

