--Add specified length for fields that are known and various keys if necessary
CREATE TABLE cities(cityId integer, city text, province text);
CREATE TABLE managers(id integer, username text, password text, restId integer, lastRestId integer);
CREATE TABLE persons(id integer,firstname text,lastname text,gender text, phone char(14), email text, username text , password text, dob char(10), priviledge integer);
CREATE TABLE province(provinceId char(2), name text);
CREATE TABLE restaurants(restId integer,name text,dateAdded char(10),menuDesc text,websites text,latitude text,longitude text,cityId integer ,address text ,postalCode text,taco_burrito integer,priceRangeAvg integer, avgReview float, phoneNo char(14),num_reviews integer);
CREATE TABLE reviews(userid integer, restId integer, stars integer);


alter table cities add constraint keys4 primary key(cityId);
alter table persons add constraint keys3 primary key(id);
alter table province add constraint keys2 primary key(provinceId);
alter table restaurants add constraint keys primary key(restId);
alter table restaurants add constraint restref foreign key(cityId) references cities(cityId);
alter table managers add constraint restrefs foreign key(restId) references restaurants(restId );
alter table managers add constraint lastrestrefs foreign key(lastRestId) references restaurants(restId);
alter table reviews add constraint personref foreign key(userId) references persons(id );
alter table reviews add constraint restrefrev foreign key(restId) references restaurants(restId );
alter table cities add constraint provref foreign key(province) references province(provinceId);
create trigger avg_review on reviews
after insert 
as 
begin 
update restaurants
set restaurants.avgReview = ((restaurants.avgReview * restaurants.reviewCount) + I.stars)/restaurants.reviewCount + 1, restaurants.reviewCount = restaurants.reviewCount+1
from inserted I 
where I.restId = restaurants.restId;

\copy  province(provinceId , name ) from /home/saurabh/COL362_Project/cleaned_data/province.csv delimiter ',' CSV HEADER;
\copy  cities(cityId , city , province ) from /home/saurabh/COL362_Project/cleaned_data/cities.csv delimiter ',' CSV HEADER;
\copy  persons(id ,firstname ,lastname ,gender , phone , email , username  , password , dob , priviledge ) from /home/saurabh/COL362_Project/cleaned_data/persons.csv delimiter ',' CSV HEADER;
\copy  restaurants(restId ,name ,dateAdded ,menuDesc ,websites ,latitude ,longitude ,cityId  ,address  ,postalCode ,taco_burrito ,priceRangeAvg , avgReview , phoneNo,num_reviews) from /home/saurabh/COL362_Project/cleaned_data/restaurants.csv delimiter ',' CSV HEADER;
\copy  managers(id , username , password , restId , lastRestId ) from /home/saurabh/COL362_Project/cleaned_data/managers.csv delimiter ',' CSV HEADER;
\copy  reviews(userId , restId , stars ) from /home/saurabh/COL362_Project/cleaned_data/reviews.csv delimiter ',' CSV HEADER;
-- BASIC QUERIES--




--COMBINATION--




