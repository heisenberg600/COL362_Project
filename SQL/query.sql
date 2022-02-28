--Add specified length for fields that are known and various keys if necessary
CREATE TABLE cities(cityId integer, city text, province text);
CREATE TABLE managers(id integer, username text, password text, restId integer, lastRestId integer);
CREATE TABLE persons(id integer,firstname text,lastname text,gender text, phone char(14), email text, username text , password text, dob char(10), priviledge integer);
CREATE TABLE province(provinceId char(2), name text);
CREATE TABLE restaurants(restId text,name text,dateAdded char(10),menuDesc text,websites text,latitude text,longitude text,cityId integer ,address text ,postalCode integer,taco_burrito integer,priceRangeAvg integer, avgReview integer, phoneNo char(14));
CREATE TABLE reviews(userId integer, restId integer, stars integer);

-- create trigger avg_review on reviews
-- after insert 
-- as 
-- begin 
-- update restaurants
-- set restaurants.avgReview = ((restaurants.avgReview * restaurants.reviewCount) + I.stars)/restaurants.reviewCount + 1, restaurants.reviewCount = restaurants.reviewCount+1
-- from inserted I 
-- where I.restId = restaurants.restId;

-- BASIC QUERIES--

--LOCATE--

-- DECLARE @TestVariable AS VARCHAR(100)
-- SET @TestVariable = 100.100

--distance--
-- select *
-- from restaurants
-- where 


--review


-- "select * from restaurants 
-- where degrees(acos(sin(radians({0})) * sin(radians({1}))) + (cos(radians({0})) * cos(radians({1})) * cos(radians({2}- {3}))))*60 * 1.1515*1.609344 < 10".format(latitude1, latitude2, longitude1, longitude2)



--username password ke base pr saari--


