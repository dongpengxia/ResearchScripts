# -*- coding: utf-8 -*-

"""
This program parses a local HTML file containing the HTML code with pending court case information, makes a list for
each category, then creates a text file for excel usage.
"""

#import statements
from bs4 import BeautifulSoup

#HOME_FILE is the location of the local HTML file
HOME_FILE = "" #Fill in

#Location of file to contain all the information in tabbed format
PENDING_CASES_TAB_FILE = '' #Fill in with location of output text file


#get html code from file in lxml soup format
with open(HOME_FILE, 'r') as openfh:
    soup = BeautifulSoup(openfh, 'lxml')


#CaseNames is a list of Case Names
CaseNames = []
#SupervisionMethods is a list of Supervision Methods
SupervisionMethods = []
#AppNos is a list of Application Numbers
AppNos = []
#StartDates is a list of Start Dates
StartDates = []
#EndDates is a list of End Dates
EndDates = []
#LetterCodes is a list of Letter Codes
LetterCodes = []
#BulletPoints is a list of Bullet Points
BulletPoints = []
#Lead is a list of whether a pending case has "(LEAD)" in its name
Lead = []


#get Case Names
count = 0
for item in soup.find_all("b"):
    count += 1
    if count % 2 == 0:
        CaseNames.append(item.get_text().encode('utf8'))
print (count/2), "Case Names"


#get Supervision Methods
count = 0
for item in soup.get_text().replace('\t','').splitlines():
    if item.replace(' ','') != '' and ('NEW CASE' in item or 'SUPERVISION' in item):
        count += 1
        SupervisionMethods.append(item.strip(' '))
print count, "Supervision Methods"


#get Application Numbers and Letter Codes
count = 0
for item in soup.find_all("a", {"href": "javascript:;"})[:-1]:
    count += 1
    if count % 2 == 1:
        AppNos.append(item.get_text().strip('\n').strip('\t').strip(' ').strip('\t').replace(',',';').replace('\n',''))
    else:
        LetterCodes.append(item.get_text().strip('\n').strip('\t').strip(' ').strip('\t').replace(',',';').replace('\n',''))
print count, "Application Numbers and Letter Codes"


#get Start Dates
count = 0
for item in soup.get_text().replace('\t','').splitlines():
    if item.replace(' ','') != '' and item.count('/') > 1 and len(item) == 26:
        count += 1
        str = item[:10].split('/')[1] + "/" +item[:10].split('/')[0] + "/" + item[:10].split('/')[2]
        StartDates.append(str)
print count, "Start Dates"


#get End Dates
count = 0
for item in soup.find_all("font", {"class": "judgment-result-final-date"}):
    count += 1
    str = item.get_text().replace(' ','').split('/')[1] + "/" + item.get_text().replace(' ','').split('/')[0] + "/" + item.get_text().replace(' ','').split('/')[2]
    EndDates.append(str)
print count, "End Dates"


#get Bullet Points
count = 0
for item in soup.find_all("div", {"class": "balloonstyle"}):
    str = ""
    count += 1
    for info in item.find_all("li"):
         str = str + info.get_text().strip('\t').strip('\n').strip(' ').encode('utf8') + ';'
    BulletPoints.append(str.replace(';;',';').replace(';;',';').replace(';;',';').replace(';;',';'))
print count, "Bullet Points"


#get Lead
count = 0
num = 0
for item in soup.get_text().replace('\t','').splitlines():
    if item.replace(' ','') != '' and "v." in item:
        count += 1
        if "LEAD" in item:
            Lead.append('1')
            num += 1
        else:
            Lead.append('0')
print count, "Pending Cases"
print num, "Pending Cases with (LEAD)"





#t is the file to contain all the pending cases in tabbed format
t = open(PENDING_CASES_TAB_FILE, 'w')

#write category titles to file t
t.write('Case Name')
t.write('\t')
t.write('Supervision Method')
t.write('\t')
t.write('App. No.')
t.write('\t')
t.write('Start Date')
t.write('\t')
t.write('End Date')
t.write('\t')
t.write('Letter Code')
t.write('\t')
t.write('Bullet Points')
t.write('\t')
t.write('(LEAD)?')
t.write('\n')

for i in range(len(CaseNames)):
    t.write(CaseNames[i])
    t.write('\t')
    t.write(SupervisionMethods[i])
    t.write('\t')
    t.write(AppNos[i])
    t.write('\t')
    t.write(StartDates[i])
    t.write('\t')
    t.write(EndDates[i])
    t.write('\t')
    t.write(LetterCodes[i])
    t.write('\t')
    t.write(BulletPoints[i].strip(';'))
    t.write('\t')
    t.write(Lead[i])
    t.write('\n')

t.close()




#Debugging by printing
#First Dates and Second Dates
"""
count = 0
for item in soup.get_text().replace('\t','').splitlines():
    if item.replace(' ','') != '' and item.count('/') > 1 and len(item) == 26:
        count += 1
        print item[:10]
print count
#3152 items
"""

#SUPERVISION
"""
count = 0
for item in soup.get_text().replace('\t','').splitlines():
    if item.replace(' ','') != '' and ('NEW CASE' in item or 'SUPERVISION' in item):
        count += 1
        print item.strip(' ')
print count
#3152 items
"""

#Bullet points
"""
count = 0
for item in soup.find_all("div", {"class": "balloonstyle"}):
    count += 1
    for info in item.find_all("li"):
        print info.get_text().strip('\t').strip('\n'), ';',
    print '\n'
print count
#3152 items
"""

#case names
"""
count = 0
for item in soup.find_all("b"):
    count += 1
    if count % 2 == 0:
        print item.get_text()
print count
#3152 items
"""

#second dates
"""
count = 0
for item in soup.find_all("font", {"class": "judgment-result-final-date"}):
    count += 1
    print item.get_text().replace(' ','')
print count
#3152 items
"""

#application numbers and RA
"""
count = 0
for item in soup.find_all("a", {"href": "javascript:;"})[:-1]:
    count += 1
    print item.get_text().strip('\n').strip('\t').strip(' ').strip('\t').replace(',',';').replace('\n','')
print count
#3152 pairs
"""

#LEAD Yes or No
"""
count = 0
num = 0
for item in soup.get_text().replace('\t','').splitlines():
    if item.replace(' ','') != '' and "v." in item:
        count += 1
        if "LEAD" in item:
            print 1
            num += 1
        else:
            print 0
print count
#3152 items
print num
#412 LEADs
"""