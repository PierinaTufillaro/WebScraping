from flask import Flask, jsonify, request 

#To work with meta tags
import requests
from bs4 import BeautifulSoup
from requests import get

#To work with .csv files
import csv
import codecs

#To get the keyword with maximum appearances
import operator

app = Flask(__name__)

#Counts the amount of keywords that the title has
def keywordsInTitle(kList,title):
	count = 0
	for keyword in kList:
		if keyword in title:
			count = count + 1
	return count

#Gets the frequency of keywords
def countingKeywords(klist):
	freq = {} 
	for items in klist:
		freq[items] = klist.count(items) 
	return freq

#Returns the keywords that appears once
def uniqueKeywords(klist):
	result = []
	for items in klist:
		if klist[items] == 1:
			result.append(items)
	return len(result)

#This endpoint gets the keywords of a webpage that gets from parameter and returns the statistics
#In some pages are stored in a meta tag named 'kewords', and in others with name = 'keyword'
@app.route('/keywords', methods=['POST'])
def keywords():
	req_Json = request.get_json() 
	page = req_Json['page']
	data = {}
	try:
		#Gets the keywords
		res = requests.get(page).text
		soup = BeautifulSoup(res, "html.parser")
		title = soup.find('title').string
		meta_list= soup.find_all('meta',{'name':'keywords'})
		#If it doesn't find anything, search with 'keyword' name
		if not meta_list:
			meta_list= soup.find_all('meta',{'name':'keyword'})
		#If meta_list is not empty, it will get all the keywords
		#and then make the statistics
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
			data['Unique Keywords'] = uniqueKeywords(keywordsFrequency)
			data['Keyword with maximum appearances'] =  max(keywordsFrequency.items(), key=operator.itemgetter(1))[0]
		else:
			data['Keywords In Title']= 'No keywords'
			data['Keywords Frequency'] = 'No keywords'
			data['Unique Keywords'] = 'No keywords'
		return jsonify(data)
	except Exception as exception:
			return ("Ocurrio una excepcion: " + str(exception))	

#This endpoint returns the title of a webpage send by a parameter
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

#This endpoint process a .csv file that contents urls.
#It returns the title of those urls.
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

#Delete the following pound keys to try the endpoint that process
#the .csv files

#	csv_path = 'sample_urls.csv'
#	with open(csv_path, "rb") as f_obj:
#		csv_reader(codecs.iterdecode(f_obj, 'utf-8'))
	app.run(debug=True, port=5000)