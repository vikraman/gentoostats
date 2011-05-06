
-- run as 'vh4x0r'@'localhost' identified by 'vh4x0r'
use gentoostats;

drop table if exists hosts;
create table hosts (
  uuid varchar (40) primary key,
  passwd varchar (40) not null
);

drop table if exists env;
create table env (
  uuid varchar (40) references hosts.uuid,
  var varchar (15) not null,
  value varchar (100),
  primary key (uuid, var)
);

drop table if exists packages;
create table packages (
  cat varchar (20) not null,
  pkg varchar (20) not null,
  ver varchar (20) not null,
  pkey serial primary key
);

drop table if exists useflags;
create table useflags (
  uuid varchar (40) references host.uuid,
  useflag varchar (20) not null,
  pkey serial references packages.pkey
);
