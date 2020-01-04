import pandas as pd
import pyodbc
from database_information import *

#Establishing connection with SQL Server database
conn = pyodbc.connect('Driver={'+DRIVER_NAME+'}; Server='+SERVER_NAME+', '+str(PORT)+';Database='+DATABASE_NAME+';UID='+USER+'; PWD='+PASSWORD+';')
conn.setencoding(encoding='utf-8')

# Retrieving data from Excel
xls = pd.ExcelFile('dados.xlsx')
factor_sheet = pd.read_excel(xls, 'Fatores')
product_sheet = pd.read_excel(xls, 'Produtos')
sale_sheet = pd.read_excel(xls, 'Vendas')
customer_sheet = pd.read_excel(xls, 'Clientes')

#Inserting in database tables from data extracted of the Excel file
cursor = conn.cursor()
product_mapping = {}
city_mapping = {}
customer_mapping = {}

# PRODUCT
counter = 0
for index, product in product_sheet.iterrows():
	counter += 1
	product_mapping[product.Nome] = counter
	cursor.execute("INSERT INTO "+DATABASE_NAME+".dbo.Product VALUES ("+str(counter)+", '"+product.Nome+"', "+str(product.Preço)+")")
	conn.commit()

# FACTOR
counter = 0
for index, factor in factor_sheet.iterrows():
	counter += 1
	cursor.execute("INSERT INTO "+DATABASE_NAME+".dbo.Factor VALUES ("+str(counter)+", '"+factor.Nome+"', "+str(factor.Porcentagem)+")")
	conn.commit()

# CITY
customer_sheet["Local"] = customer_sheet["Cidade"] + '/' + customer_sheet['Estado'] 
cities_list = customer_sheet.Local.unique()
counter = 0
for localization in cities_list:
	counter += 1
	city, state = localization.split('/')
	city_mapping[city] = counter
	cursor.execute("INSERT INTO "+DATABASE_NAME+".dbo.City VALUES ("+str(counter)+", '"+city+"', '"+state+"')")
	conn.commit()

# CUSTOMER
counter = 0
for index, customer in customer_sheet.iterrows():
	counter += 1
	first_name, last_name = customer.Cliente.split(' ')
	customer_mapping[customer.Cliente] = counter
	cursor.execute("INSERT INTO "+DATABASE_NAME+".dbo.Customer VALUES ("+str(counter)+", "+str(city_mapping[customer.Cidade])+", '"+first_name+"', '"+last_name+"')")
	conn.commit()

# SALE // SALE COMMENT
# This specific table, sale comment, is described with a none or many to one relationship with sale table
# Nevertheless, the data provided has only sales with 0 or 1 comments. Due to that, implementation is simplified.
counter = 0
comments_counter = 0
for index, sale in sale_sheet.iterrows():
	counter += 1
	cursor.execute("INSERT INTO "+DATABASE_NAME+".dbo.Sale VALUES ("+str(counter)+", "+str(customer_mapping[sale.Cliente])+", "+str(product_mapping[sale.Produto])+", "+str(sale.Preço)+", "+str(sale.Quantidade)+")")
	conn.commit()
	if (len(str(sale.Comentário).split(' ', 1)) > 1):
		comment_date, comment = sale.Comentário.split(' ', 1)
		comments_counter += 1
		cursor.execute("INSERT INTO "+DATABASE_NAME+".dbo.SaleComment VALUES ("+str(comments_counter)+", "+str(counter)+", "+str(customer_mapping[sale.Cliente])+", '"+comment_date+"', '"+comment+"')")
		conn.commit()

conn.close()