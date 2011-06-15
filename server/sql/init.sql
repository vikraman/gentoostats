
-- run as 'gentoo'@'localHOST' identified by 'gentoo'
use `gentoostats`;

drop table if exists `ENV`;
drop table if exists `GLOBAL_KEYWORDS`;
drop table if exists `HOST_LANG`;
drop table if exists `HOST_FEATURES`;
drop table if exists `HOST_MIRRORS`;
drop table if exists `GLOBAL_USEFLAGS`;
drop table if exists `PLUS_USEFLAGS`;
drop table if exists `MINUS_USEFLAGS`;
drop table if exists `UNSET_USEFLAGS`;
drop table if exists `INSTALLED_PACKAGES`;
drop table if exists `LANG`;
drop table if exists `FEATURES`;
drop table if exists `GENTOO_MIRRORS`;
drop table if exists `USEFLAGS`;
drop table if exists `KEYWORDS`;
drop table if exists `PACKAGES`;
drop table if exists `REPOSITORIES`;
drop table if exists `HOSTS`;

create table `HOSTS` (
  `UUID` binary (16),
  `PASSWD` varchar (32) not null,
  primary key (`UUID`)
) engine=innodb;

create table `ENV` (
  `UUID` binary (16),
  `PLATFORM` varchar (128),
  `ARCH` varchar (16),
  `CHOST` varchar (32),
  `CFLAGS` varchar (64),
  `CXXFLAGS` varchar (64),
  `FFLAGS` varchar (64),
  `LDFLAGS` varchar (64),
  `MAKEOPTS` varchar (8),
  `LASTSYNC` varchar(32),
  `PROFILE` varchar (64),
  `SYNC` varchar (128),
  primary key (`UUID`),
  foreign key (`UUID`) references `HOSTS`(`UUID`)
  on delete cascade on update cascade
) engine=innodb;

create table `KEYWORDS` (
  `KWKEY` serial,
  `KEYWORD` varchar (16),
  primary key (`KEYWORD`)
) engine=innodb;

create table `GLOBAL_KEYWORDS` (
  `UUID` binary (16),
  `KWKEY` bigint unsigned,
  primary key (`UUID`, `KWKEY`),
  foreign key (`UUID`) references `HOSTS`(`UUID`)
  on delete cascade on update cascade,
  foreign key (`KWKEY`) references `KEYWORDS`(`KWKEY`)
  on delete cascade on update cascade
) engine=innodb;

create table `LANG` (
  `LKEY` serial,
  `LANG` varchar (16),
  primary key (`LANG`)
) engine=innodb;

create table `HOST_LANG` (
  `UUID` binary (16),
  `LKEY` bigint unsigned,
  primary key (`UUID`, `LKEY`),
  foreign key (`UUID`) references `HOSTS`(`UUID`)
  on delete cascade on update cascade,
  foreign key (`LKEY`) references `LANG`(`LKEY`)
  on delete cascade on update cascade
) engine=innodb;

create table `FEATURES` (
  `FKEY` serial,
  `FEATURE` varchar (64),
  primary key (`FEATURE`)
) engine=innodb;

create table `HOST_FEATURES` (
  `UUID` binary (16),
  `FKEY` bigint unsigned,
  primary key (`UUID`, `FKEY`),
  foreign key (`UUID`) references `HOSTS`(`UUID`)
  on delete cascade on update cascade,
  foreign key (`FKEY`) references `FEATURES`(`FKEY`)
  on delete cascade on update cascade
) engine=innodb;

create table `GENTOO_MIRRORS` (
  `MKEY` serial,
  `MIRROR` varchar (128),
  primary key (`MIRROR`)
) engine=innodb;

create table `HOST_MIRRORS` (
  `UUID` binary (16),
  `MKEY` bigint unsigned,
  primary key (`UUID`, `MKEY`),
  foreign key (`UUID`) references `HOSTS`(`UUID`)
  on delete cascade on update cascade,
  foreign key (`MKEY`) references `GENTOO_MIRRORS`(`MKEY`)
  on delete cascade on update cascade
) engine=innodb;

create table `PACKAGES` (
  `PKEY` serial,
  `CAT` varchar (32),
  `PKG` varchar (64),
  `VER` varchar (32),
  primary key (`CAT`, `PKG`, `VER`)
) engine=innodb;

create table `REPOSITORIES` (
  `RKEY` serial,
  `REPO` varchar (32),
  primary key (`REPO`)
) engine=innodb;

create table `INSTALLED_PACKAGES` (
  `IPKEY` serial,
  `UUID` binary (16),
  `PKEY` bigint unsigned,
  `BUILD_TIME` bigint unsigned,
  `COUNTER` bigint unsigned,
  `KWKEY` bigint unsigned,
  `RKEY` bigint unsigned,
  `SIZE` bigint unsigned,
  primary key (`UUID`, `PKEY`),
  foreign key (`UUID`) references `HOSTS`(`UUID`)
  on delete cascade on update cascade,
  foreign key (`PKEY`) references `PACKAGES`(`PKEY`)
  on delete cascade on update cascade,
  foreign key (`KWKEY`) references `KEYWORDS`(`KWKEY`)
  on delete cascade on update cascade,
  foreign key (`RKEY`) references `REPOSITORIES`(`RKEY`)
  on delete cascade on update cascade
) engine=innodb;

create table `USEFLAGS` (
  `UKEY` serial,
  `USEFLAG` varchar (64),
  primary key (`USEFLAG`)
) engine=innodb;

create table `GLOBAL_USEFLAGS` (
  `UUID` binary (16),
  `UKEY` bigint unsigned,
  primary key (`UUID`, `UKEY`),
  foreign key (`UUID`) references `HOSTS`(`UUID`)
  on delete cascade on update cascade,
  foreign key (`UKEY`) references `USEFLAGS`(`UKEY`)
  on delete cascade on update cascade
) engine=innodb;

create table `PLUS_USEFLAGS` (
  `IPKEY` bigint unsigned,
  `UKEY` bigint unsigned,
  primary key (`IPKEY`, `UKEY`),
  foreign key (`IPKEY`) references `INSTALLED_PACKAGES`(`IPKEY`)
  on delete cascade on update cascade,
  foreign key (`UKEY`) references `USEFLAGS`(`UKEY`)
  on delete cascade on update cascade
) engine=innodb;

create table `MINUS_USEFLAGS` (
  `IPKEY` bigint unsigned,
  `UKEY` bigint unsigned,
  primary key (`IPKEY`, `UKEY`),
  foreign key (`IPKEY`) references `INSTALLED_PACKAGES`(`IPKEY`)
  on delete cascade on update cascade,
  foreign key (`UKEY`) references `USEFLAGS`(`UKEY`)
  on delete cascade on update cascade
) engine=innodb;

create table `UNSET_USEFLAGS` (
  `IPKEY` bigint unsigned,
  `UKEY` bigint unsigned,
  primary key (`IPKEY`, `UKEY`),
  foreign key (`IPKEY`) references `INSTALLED_PACKAGES`(`IPKEY`)
  on delete cascade on update cascade,
  foreign key (`UKEY`) references `USEFLAGS`(`UKEY`)
  on delete cascade on update cascade
) engine=innodb;
