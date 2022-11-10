create database user_details
use user_details
create table userdetails
(
userID int primary key,
username varchar(50),
password varchar(50),
email varchar(50),
rollno int
)
insert into userdetails values (1,'Eswar','Eswar123','eswar@gmail.com',810019205034);
select * from userdetails