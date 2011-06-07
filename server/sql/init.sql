
-- run as 'gentoo'@'localhost' identified by 'gentoo'
use `gentoostats`;

drop table if exists `hosts`;
create table `hosts` (
  `uuid` binary (16),
  `passwd` varchar (32) not null,
  primary key (`uuid`)
);

drop table if exists `env`;
create table `env` (
  `uuid` binary (16) references hosts.uuid,
  `platform` varchar (128),
  `arch` varchar (16),
  `chost` varchar (32),
  `cflags` varchar (64),
  `cxxflags` varchar (64),
  `fflags` varchar (64),
  `ldflags` varchar (64),
  `makeopts` varchar (8),
  `lastsync` timestamp,
  `profile` varchar (64),
  `sync` varchar (128),
  primary key (`uuid`)
);

drop table if exists `keywords`;
create table `keywords` (
  `kwkey` serial,
  `keyword` varchar (16),
  primary key (`keyword`)
);

drop table if exists `global_keywords`;
create table `global_keywords` (
  `uuid` binary (16) references hosts.uuid,
  `kwkey` bigint unsigned references keywords.kwkey,
  primary key (`uuid`, `kwkey`)
);

drop table if exists `lang`;
create table `lang` (
  `lkey` serial,
  `lang` varchar (16),
  primary key (`lang`)
);

drop table if exists `host_lang`;
create table `host_lang` (
  `uuid` binary (16) references hosts.uuid,
  `lkey` bigint unsigned references lang.lkey,
  primary key (`uuid`, `lkey`)
);

drop table if exists `features`;
create table `features` (
  `fkey` serial,
  `feature` varchar (64),
  primary key (`feature`)
);

drop table if exists `host_features`;
create table `host_features` (
  `uuid` binary (16) references hosts.uuid,
  `fkey` bigint unsigned references features.fkey,
  primary key (`uuid`, `fkey`)
);

drop table if exists `gentoo_mirrors`;
create table `gentoo_mirrors` (
  `mkey` serial,
  `mirror` varchar (128),
  primary key (`mirror`)
);

drop table if exists `host_mirrors`;
create table `host_mirrors` (
  `uuid` binary (16) references hosts.uuid,
  `mkey` bigint unsigned references gentoo_mirrors.mkey,
  primary key (`uuid`, `mkey`)
);

drop table if exists `packages`;
create table `packages` (
  `pkey` serial,
  `cat` varchar (32),
  `pkg` varchar (64),
  `ver` varchar (32),
  primary key (`cat`, `pkg`, `ver`)
);

drop table if exists `repositories`;
create table `repositories` (
  `rkey` serial,
  `repo` varchar (32),
  primary key (`repo`)
);

drop table if exists `installed_packages`;
create table `installed_packages` (
  `ipkey` serial,
  `uuid` binary (16) references hosts.uuid,
  `pkey` bigint unsigned references packages.pkey,
  `build_time` timestamp,
  `counter` bigint unsigned,
  `kwkey` bigint unsigned references keywords.kwkey,
  `rkey` varchar (64) references repositories.rkey,
  `size` bigint unsigned,
  primary key (`uuid`, `pkey`)
);

drop table if exists `useflags`;
create table `useflags` (
  `ukey` serial,
  `useflag` varchar (64),
  primary key (`useflag`)
);

drop table if exists `global_useflags`;
create table `global_useflags` (
  `uuid` binary (16) references hosts.uuid,
  `ukey` bigint unsigned references useflags.ukey,
  primary key (`uuid`, `ukey`)
);

drop table if exists `plus_useflags`;
create table `plus_useflags` (
  `ipkey` bigint unsigned references installed_packages.ipkey,
  `ukey` bigint unsigned references useflags.ukey,
  primary key (`ipkey`, `ukey`)
);

drop table if exists `minus_useflags`;
create table `minus_useflags` (
  `ipkey` bigint unsigned references installed_packages.ipkey,
  `ukey` bigint unsigned references useflags.ukey,
  primary key (`ipkey`, `ukey`)
);

drop table if exists `unset_useflags`;
create table `unset_useflags` (
  `ipkey` bigint unsigned references installed_packages.ipkey,
  `ukey` bigint unsigned references useflags.ukey,
  primary key (`ipkey`, `ukey`)
);
