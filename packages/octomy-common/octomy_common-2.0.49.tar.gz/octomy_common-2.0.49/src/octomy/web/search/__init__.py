from bs4 import BeautifulSoup
import logging
import os
import jellyfish
import pprint


logger = logging.getLogger(__name__)


def file_to_list(fn):
	out=[]
	with open(fn, "r") as f:
		for line in f:
			out.append(line.strip())
	return out


def spread_keywords(keywords, w):
	adds = []
	for i in range(0, len(keywords)-w):
		add=[]
		for j in range(0, w):
			add.append(keywords[i+j])
		adds.append(" ".join(add))
	return adds


phonetic_identifier="🚡"
def phonify(keyword):
	return [
		  f"{phonetic_identifier}{keyword.lower()}"
		, f"{phonetic_identifier}{jellyfish.soundex(keyword)}"
		, f"{phonetic_identifier}{jellyfish.nysiis(keyword)}"
#		, f"{phonetic_identifier}{jellyfish.match_rating_codex(keyword)}"
		, f"{phonetic_identifier}{jellyfish.metaphone(keyword)}"
	#   , f"{phonetic_identifier}{jellyfish.porter_stem}"
	]
 
def decorate_keywords(keywords):
	phonetic = []
	for keyword in keywords:
		if keyword:
			phonetic += phonify(keyword)
	return phonetic

def stopword_filtered(keywords, stopwords):
	out=[]
	for keyword in keywords:
		if keyword not in stopwords:
			out.append(keyword)
	return out
 

def saturate_keywords(keywords, stopwords):
	filtered = stopword_filtered(keywords, stopwords)
	for i in range(2, 5):
		keywords += spread_keywords(keywords, i)
		keywords += spread_keywords(filtered, i)
	keywords += decorate_keywords(keywords)
	keywords += decorate_keywords(filtered)
	return keywords



class SearchEngine:
	def __init__(self):
		self.page_index={}
		self.page_text={}
		self.page_title={}
		self.page_text_index={}
		self.stopwords=file_to_list(f"{os.path.dirname(__file__)}/stopwords.txt")
		#logger.info("STOPWORDS:")
		#logger.info(", ".join(self.stopwords))
		#logger.info(f"INDEX: {pprint.pformat(self.page_index)}")

	def index_page(self, path):
		html, err = handler_raw(path)
		if err:
			logger.error(f"SKIPPING PAGE {path}")
			return False
		soup = BeautifulSoup(html)
		title = soup.title.get_text()
		page_title[path] = title
		text = soup.get_text()
		keywords = text.split()
		text = " ".join(keywords)
		page_text[path] = text
		keywords = saturate_keywords(keywords, self.stopwords)
		counts = {}
		for keyword in keywords:
			counts[keyword] = counts.get(keyword, 0) + 1
		#logger.info(f"Indexed {path} into:")
		#logger.info(pprint.pformat(text))
		#logger.info(pprint.pformat(counts))
		for keyword in keywords:
			count = counts.get(keyword, 1)
			pages = page_index.get(keyword, dict())
			pages[path] = count + pages.get(path, 0)
			page_index[keyword] = pages
		for keyword in keywords:
			pages = page_text_index.get(keyword, dict())
			hit=text.find(keyword)
			if -1 != hit:
				pages[path] = hit
			page_text_index[keyword] = pages
		return True
	
	def summarize(self, keyword, path, width=10):
		pages = page_text_index.get(keyword, dict())
		index = pages.get(path, None)
		if index:
			text = page_text.get(path, None)
			if text:
				s = index-width
				l = len(keyword)+width*2
				logger.info(f"s={s},l={l}")
				return text[s:l]
		return ""
	
	def find_in_index(self, q, max=10):
		if not q or ""==q:
			return ""
		ret = {}
		score = 0
		saturated_q = saturate_keywords([q], self.stopwords)
		logger.info(f"saturated q: {pprint.pformat(saturated_q)} ############################")
		for s in saturated_q:
			hits = page_index.get(s, dict())
			logger.info(f"hits for {s}: {pprint.pformat(hits)}")
			for path, count in hits.items():
				ret[path] = count + ret.get(path, 0)
		logger.info(f"Total: {pprint.pformat(ret)}")
		logger.info("")
		return ret
	
	
	
	def federated_search(self, q:str):
		ret = find_in_index(q)
		logger.info(f"HIT:{pprint.pformat(ret)}")
		out=[]
		for path, score in ret.items():
			hit = [score # Score
			, page_title.get(path, "Unknown") # Title
			, self.summarize(q, path) #Context
			, 6 # Beginning
			, 5 # length
			, path # Link URL
			]
			out.append(hit)
