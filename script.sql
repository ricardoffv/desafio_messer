---------------------------------------------------------------
-- DATABASE CREATION
---------------------------------------------------------------
CREATE DATABASE Sales;
USE Sales;

CREATE TABLE PRODUCT (
	ProductId	INT NOT NULL PRIMARY KEY,
	Name		VARCHAR(255) NOT NULL,
	Price		DECIMAL(10,2) NOT NULL
);

CREATE TABLE FACTOR (
	FactorId	INT NOT NULL PRIMARY KEY,
	Name		VARCHAR(255) NOT NULL,
	Percentage	DECIMAL(15,5) NOT NULL
);

CREATE TABLE CITY (
	CityId		INT NOT NULL PRIMARY KEY,
	Name		VARCHAR(255) NOT NULL,
	State		VARCHAR(255) NOT NULL
);

CREATE TABLE CUSTOMER (
	CustomerId	INT NOT NULL PRIMARY KEY,
	CityId		INT FOREIGN KEY REFERENCES CITY(CityId),
	FirstName	VARCHAR(255) NOT NULL,	
	LastName	VARCHAR(255) NOT NULL
);

CREATE TABLE SALE (
	SaleId		INT NOT NULL PRIMARY KEY,
	CustomerId	INT FOREIGN KEY REFERENCES CUSTOMER(CustomerId),
	ProductId	INT FOREIGN KEY REFERENCES PRODUCT(ProductId),	
	Price		DECIMAL(10,2) NOT NULL,	
	Amount		INT NOT NULL
);

CREATE TABLE SALECOMMENT (
	CommentId	INT NOT NULL PRIMARY KEY,
	SaleId		INT FOREIGN KEY REFERENCES SALE(SaleId),
	CustomerId	INT FOREIGN KEY REFERENCES CUSTOMER(CustomerId),
	CommentDate	DATETIME NOT NULL,	
	CommentText	VARCHAR(255) NOT NULL
);

CREATE TABLE IGPM (
	IgpmId		INT NOT NULL PRIMARY KEY,
	Month		INT NOT NULL,
	Year		INT NOT NULL,
	Rate		DECIMAL(15,4) NOT NULL
);

------------------------------------------------------------
--PROCEDURES
------------------------------------------------------------
CREATE OR ALTER PROCEDURE UpdateFactors(
	@tax1 DECIMAL(15,5),
	@tax2 DECIMAL(15,5),
	@discount1 DECIMAL(15,5),
	@serviceCharge DECIMAL(15,5)
) AS
BEGIN TRANSACTION
-- For a better experience, this procedure updates all the factors with one line by a stored procedure call
-- It receives four parameters, in order, the factors stored in Factor table

	UPDATE Factor
	SET Percentage = @tax1	
	WHERE Name LIKE 'Imposto 1';
	UPDATE Factor
	SET Percentage = @tax2	
	WHERE Name LIKE 'Imposto 2';
	UPDATE Factor
	SET Percentage = @discount1	
	WHERE Name LIKE 'Desconto 1';
	UPDATE Factor
	SET Percentage = @serviceCharge	
	WHERE Name LIKE 'Taxa de serviço';
	
COMMIT TRANSACTION

CREATE OR ALTER PROCEDURE UpdatePrices
AS
BEGIN TRANSACTION
-- This procedure updates all products according to the sum of factors in Factor Table, which acts a multiplying factor on the prices. 
	UPDATE Product
	SET Price = (SELECT SUM(Percentage) FROM Factor) * Price;

COMMIT TRANSACTION
