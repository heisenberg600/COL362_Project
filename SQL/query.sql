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
alter table managers add constraint personrefman foreign key(id) references persons(id ) on delete cascade;
alter table managers add constraint lastrestrefs foreign key(lastRestId) references restaurants(restId);
alter table reviews add constraint personref foreign key(userId) references persons(id ) on delete cascade;
alter table reviews add constraint restrefrev foreign key(restId) references restaurants(restId );
alter table cities add constraint provref foreign key(province) references province(provinceId);



\copy  province(provinceId , name ) from /home/mrstark/Desktop/COL362/Project/cleaned_data/province.csv delimiter ',' CSV HEADER;
\copy  cities(cityId , city , province ) from /home/mrstark/Desktop/COL362/Project/cleaned_data/cities.csv delimiter ',' CSV HEADER;
\copy  persons(id ,firstname ,lastname ,gender , phone , email , username  , password , dob , priviledge ) from /home/mrstark/Desktop/COL362/Project/cleaned_data/persons.csv delimiter ',' CSV HEADER;
\copy  restaurants(restId ,name ,dateAdded ,menuDesc ,websites ,latitude ,longitude ,cityId  ,address  ,postalCode ,taco_burrito ,priceRangeAvg , avgReview , phoneNo,num_reviews) from /home/mrstark/Desktop/COL362/Project/cleaned_data/restaurants.csv delimiter ',' CSV HEADER;
\copy  managers(id , username , password , restId , lastRestId ) from /home/mrstark/Desktop/COL362/Project/cleaned_data/managers.csv delimiter ',' CSV HEADER;
\copy  reviews(userId , restId , stars ) from /home/mrstark/Desktop/COL362/Project/cleaned_data/reviews.csv delimiter ',' CSV HEADER;

CREATE OR REPLACE FUNCTION updation()                                                                                        
RETURNS trigger
AS
$$
BEGIN

UPDATE restaurants SET avgReview = ((avgReview *num_reviews) + new.stars)/(num_reviews + 1), num_reviews = num_reviews+1; return null;
END;
$$ LANGUAGE PLPGSQL;

create trigger avg_review
after insert
on reviews
for each row
execute procedure updation();



create or replace view managersView as
select managers.id as id, managers.restId as restId, lastRestID, restaurants.name as name, priceRangeAvg, websites, phoneNo, 
    taco_burrito, menuDesc, latitude, longitude, city, province.name as pname, postalCode,cities.cityId
from managers, restaurants, cities, province
where managers.restId = restaurants.restId and restaurants.cityId = cities.cityId and cities.province = provinceId;


CREATE OR REPLACE FUNCTION managerviewtrig()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $function$
   BEGIN
	IF TG_OP = 'UPDATE' THEN
	Update restaurants set name= new.name , priceRangeAvg=new.priceRangeAvg, websites=new.websites,phoneNo=new.phoneNo, taco_burrito=new.taco_burrito, menuDesc=new.menuDesc, 	    latitude=new.latitude,longitude=new.longitude,postalCode=new.postalcode,cityId=new.cityId where restId=old.restId;
       RETURN NEW;
      ELSIF TG_OP = 'DELETE' THEN
       DELETE FROM restaurants WHERE restId=OLD.restId;
       DELETE FROM managers WHERE id=OLD.id;
       RETURN NULL;
      END IF;
      RETURN NEW;
    END;
$function$;

CREATE TRIGGER managerviewtrig
    INSTEAD OF UPDATE OR DELETE ON
      managersView FOR EACH ROW EXECUTE PROCEDURE managerviewtrig();
      
      
CREATE INDEX personIndex on persons(id);
CREATE INDEX restIndex on restaurants(restid);

--username password ke base pr saari--


