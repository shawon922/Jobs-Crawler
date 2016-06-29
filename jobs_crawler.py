# -*- coding: utf-8 -*-

"""
Crawl IT jobs from bdjobs.com
"""

#Load necessary modules
import requests
from bs4 import BeautifulSoup
import csv

#Initialize a global variable to count total jobs
totalJobs = 0

#Define a function to write into file
#Function starts from here
def writeCsvFile(data):
	#'global' keyword for using the variable initialized outside the function
	global totalJobs


	for dt in data:
		#Fetching desired content using its tag and class

		jobTitle = dt.find('div', {'class': 'job-title-text'})
		jobLink = mainSite + jobTitle.find('a', {'href': True})['href']

		jobTitleText = jobTitle.text.strip()
		companyName = dt.find('div', {'class': 'comp-name-text'}).text.strip()
		education = dt.find('div', {'class': 'edu-text-d'}).text.strip()
		experience = dt.find('div', {'class': 'exp-text-d'}).text.strip()
		deadline = dt.find('div', {'class': 'dead-text-d'}).text.strip()

		#Writing into the csv file
		try:
			csvWriter.writerow([jobTitleText, companyName, education, experience, deadline, jobLink])
		except:
			print('Exception occurred! No problem. Keep going.')
		

		#Couting total jobs
		totalJobs += 1
#Function ends here

#Open a csv file with 'write' mode
jobListFileObj = open('job-list.csv', 'w', newline='')


mainSite = 'http://jobs.bdjobs.com/'

#Job search url
url = 'http://jobs.bdjobs.com/jobsearch.asp?fcatId=8'

#Post data 'dictionary' for different crieteria.
#'fcat' for 'Job Category'
#'pg' for 'Pagination'. Value is 1 by default.
#Other keys are not being used

postData = { 'Country': '0', 
		 'MPostings': '',
		 'Newspaper': '0',
		 'fcat': '8',
		 'hidJobSearch': 'JobSearch',
		 'hidOrder': '',
		 'iCat': '0',
		 'pg': '1',
		 'qAge': '0',
		 'qDeadline': '0',
		 'qExp': '0',
		 'qJobLevel': '0',
		 'qJobNature': '0',
		 'qJobSpecialSkill': '-1',
		 'qOT': '0',
		 'qPosted': '0',
		 'txtsearch': '',
		 'ver': ''
		}


columnNames = ['Job Title', 'Company Name', 'Education', 'Experience', 'Deadline', 'Job Link']

#Creating csv writer
csvWriter = csv.writer(jobListFileObj)

#Write column name
csvWriter.writerow(columnNames)
csvWriter.writerow([''])

#post request
resp = requests.post(url, data=postData)

#send response to BeautifulSoup
html = BeautifulSoup(resp.content, 'html.parser') 

data = html.find_all('div', {'class': 'norm-jobs-wrapper'})
maxPageNo = html.find('div', {'id': 'topPagging'}).find_all('li')[-1].text.strip().replace('.', '')


#Calling the writeCsvFile function
writeCsvFile(data)

maxPageNo = int(maxPageNo)

print('Page No : 1')

pageNo = 2

while pageNo <= maxPageNo:
	print('Page No : {0}'.format(pageNo))
	
	#Assign new page no.
	postData['pg'] = pageNo

	resp = requests.post(url, data=postData)

	html = BeautifulSoup(resp.content, 'html.parser')

	data = html.find_all('div', {'class': 'norm-jobs-wrapper'})

	#Calling the writeCsvFile function
	writeCsvFile(data)
	
	#Increment page no.
	pageNo += 1

jobListFileObj.close()

print('Successfully completed!')

#Total jobs
print('Total Job : {0}'.format(totalJobs))

