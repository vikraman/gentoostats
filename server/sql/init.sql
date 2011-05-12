
-- run as 'gentoo'@'localhost' identified by 'gentoo'
use gentoostats;

drop table if exists hosts;
create table hosts (
  uuid varchar (40) primary key,
  passwd varchar (40) not null
);

drop table if exists env;
create table env (
  uuid varchar (40) references hosts.uuid,
  var varchar (20) not null,
  value varchar (512),
  primary key (uuid, var)
);

drop table if exists packages;
create table packages (
  cat varchar (40) not null,
  pkg varchar (40) not null,
  ver varchar (40) not null,
  pkey serial,
  primary key (cat, pkg, ver, pkey)
);

drop table if exists useflags;
create table useflags (
  uuid varchar (40) references host.uuid,
  useflag varchar (40) not null,
  pkey bigint unsigned references packages.pkey,
  primary key (uuid, useflag, pkey)
);
