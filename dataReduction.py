import re
import os
import sqlite3
from bs4 import BeautifulSoup,NavigableString
import subprocess

p = re.compile('&gt;&gt;[0-9]+')
mat = "&gt;&gt;>>"
a = "<div class=\"message\">"
b = "</div>"

def resget(resnum,soup2):
	targ = soup2.find("div",id=resnum)
	resss = targ.find("div",class_="message")
	resss = resss.text
	resss = resss.replace("  ","\n")
	resss = resss.replace(a,"")
	resss = resss.replace(b,"")
	return resss

i = 1
files = os.listdir()
for file in files:
	try:
		html = open(file,"r").read()
		connector = sqlite3.connect(repr(i) + ".db")
		cur = connector.cursor()
		cur.execute("CREATE TABLE data(num int,title text, anched text, anch text,hianchnumm int,anchnum int);")
		po = file.rstrip(".html")
		cur.execute("INSERT INTO data(num,anchnum) VALUES (0,?)",(po,))
		soup = BeautifulSoup(html, "lxml")
		zenres = soup.find_all("div",class_="message")
		o = 0
		ooo=1
		suretai = soup.find("title")
		suretai = suretai.string
		while o < len(zenres):
			oo = o+1 
			anka = zenres[o].find("a",target="_blank")
			if isinstance(anka,type(None)):
				o += 1
				continue
			else:
				anka = anka.string
				ankanum = anka.lstrip(mat)
				hiannkamess = resget(ankanum,soup)
				ankamess = resget(oo,soup)
				cur.execute("INSERT INTO data(num,title,anched,anch,hianchnumm,anchnum) VALUES (?,?,?,?,?,?)",(ooo,suretai,hiannkamess,ankamess,ankanum,oo))
				connector.commit()
				ooo +=1
				o += 1
				continue
		connecto = sqlite3.connect("0" + repr(i) + ".db")
		cure = connecto.cursor()
		cure.execute("CREATE TABLE data(num int,anched text);")
		iiii=1
		while iiii<1001:
			try:
				resnai = resget(iiii,soup)
				cure.execute("INSERT INTO data(num,anched) VALUES (?,?)",(iiii,resnai))
				iiii +=1
				connecto.commit()
			except:
				pass
		connecto.close()
		i += 1
	except:
		i +=1
		continue
	connector.close()
