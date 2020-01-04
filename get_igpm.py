import requests
import pyodbc
from bs4 import BeautifulSoup

# The approach will take the following steps:

# 	1. Access URL which leads to IGP-M data
url_page='http://www.ipeadata.gov.br/ExibeSerie.aspx?stub=1&serid37796=37796&serid36482=36482'

response = requests.get(url_page)

#	2. Get content from last line of information table, which should be last IGPM rate
if response.status_code == 200:
	soap = BeautifulSoup(response.text, 'html.parser')
	main_table = soap.find('table', {'class': 'dxgvControl'})
	components = main_table.findAll('td', {'class': 'dxgv'})
	last_index = len(components)-5
	rate = components[last_index].text
	rate = rate.replace(',', '.')
	year, month = components[last_index-2].text.split('.')


# 	3. Store it in Sales database
from database_information import *
conn = pyodbc.connect('Driver={'+DRIVER_NAME+'}; Server='+SERVER_NAME+', '+str(PORT)+';Database='+DATABASE_NAME+';UID='+USER+'; PWD='+PASSWORD+';')
conn.setencoding(encoding='utf-8')

cursor = conn.cursor()

# Get Identifier of next rate stored
cursor.execute("SELECT COUNT(*) AS countIGPM FROM "+DATABASE_NAME+".dbo.IGPM")

# Inserting in the database
cursor.execute("INSERT INTO "+DATABASE_NAME+".dbo.IGPM VALUES ("+str(cursor.fetchall()[0].countIGPM + 1)+", "+month+", "+year+", "+rate+")")
conn.commit()
