from flask import Flask, jsonify, request 

#Para encontrar los meta
import requests
from bs4 import BeautifulSoup
from requests import get

#Para tratar archivos csv
import csv
import codecs

app = Flask(__name__)

def keywordsInTitle(kList,title):
	count = 0
	for keyword in kList:
		if keyword in title:
			count = count + 1
	return count

def countingKeywords(klist):
	freq = {} 
	for items in klist:
		freq[items] = klist.count(items) 
	return freq

def uniqueKeywords(klist):
	result = []
	for items in klist:
		if klist[items] == 1:
			result.append(items)
	return len(result)


@app.route('/keywords', methods=['POST'])
def keywords():
	req_Json = request.get_json() 
	page = req_Json['page']
	data = {}
	try:
		res = requests.get(page).text
		soup = BeautifulSoup(res, "html.parser")
		title = soup.find('title').string
		meta_list= soup.find_all('meta',{'name':'keywords'})
		if not meta_list:
			meta_list= soup.find_all('meta',{'name':'keyword'})
		if meta_list:
			for a in meta_list:
				content = a.get('content')
			lista = (content.split(","))
			if title:
				data['Keywords In Title']= keywordsInTitle(lista,title)
			else:
				data['Keywords In Title']= 'No title'		
			keywordsFrequency = countingKeywords(lista)
			data['Keywords Frequency'] = keywordsFrequency
			keywordsOnce =  uniqueKeywords(keywordsFrequency)
			data['Unique Keywords'] = keywordsOnce
		else:
			data['Keywords In Title']= 'No keywords'
			data['Keywords Frequency'] = 'No keywords'
			data['Unique Keywords'] = 'No keywords'
		return jsonify(data)
	except Exception as exception:
			return ("Ocurrio una excepcion: " + str(exception))	

@app.route('/title', methods=['POST'])
def title():
	req_Json = request.get_json() 
	page = req_Json['page']
	try:
		res = requests.get(page).text
		soup = BeautifulSoup(res, "html.parser")
		title = soup.find('title').string
		if not title:
			return "No title"
		return str(title)
	except Exception as exception:
		return ("Ocurrio una excepcion: " + str(exception))

@app.route('/csv_reader')
def csv_reader(file_obj):
	reader = csv.reader(file_obj)
	next(reader) #Saltea la linea del titulo
	for row in reader:
		data = row[0]
		try:
			res = requests.get(data).text
			soup = BeautifulSoup(res, "html.parser")
			title = soup.find('title').string
			if not title:
				print ("NO TITLE")
			else:
				print (str(title))	
		except Exception as exception:
			print ("Ocurrio una excepcion: " + str(exception))
	print ("ok")

if __name__ == '__main__':
	csv_path = 'sample_urls.csv'
	with open(csv_path, "rb") as f_obj:
		csv_reader(codecs.iterdecode(f_obj, 'utf-8'))
	app.run(debug=True, port=5000)