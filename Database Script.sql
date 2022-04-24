drop database ARMS;
create database ARMS;
use ARMS;
create table users (username varchar(255), password varchar(255), first_name varchar(255), Last_name varchar(255), email varchar(255), phone_number varchar(255), last_login datetime, api_key varchar(255));
show tables;
select * from users;
alter table users add unique (username, api_key);
alter table users add primary key (username, api_key);
truncate users;

insert into users (username, password, first_name, last_name, email, phone_number, last_login, api_key) 
values ('blackthreat', sha2('ahlawenti', 512), 'Mohamed Ali', 'Bessaidi', 'bessaidiMohamedAli99@gmail.com', '12345678', now(), 'ahlawenti123');

create table Node (deviceID varchar(255), username varchar(255), field_name varchar(255), temperature int, humidity int, light int,
foreign key (username) references users(username), primary key (deviceID));
select * from Node;
-- select field_name, temperature, humidity, moisture, light from Node where username="amansingh";

insert into Node (deviceID, username, field_name, temperature, humidity, light)
values('Sensor_Pi', 'blackthreat', 'Sensors', 45, 54, 100);
-- insert into Node (deviceID, username, field_name, temperature, humidity, moisture, light)
-- values('ARMS22212', 'blackthreat', 'Samy Garden', 45, 54, 100, 600);

select * from Node;

create table Sensors (deviceID varchar(255), temperature int, humidity int, light int, date_time datetime,
foreign key (deviceID) references Node(deviceID));

insert into Sensors (deviceID, temperature, humidity, light, date_time)
values('Sensor_Pi', 45, 54, 600, now());

select * from users where username = "hellboy";
update users set last_login = now() where username = "hellboy";

select * from Sensors;
select * from (select * from Rosegarden order by date_time desc limit 10) dummy order by date_time asc;
select * from (select * from Rosegarden order by date_time desc limit 10) dummy order by date_time asc;
