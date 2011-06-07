
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
  `uuid` binary (16),
  `platform` varchar (128),
  `arch` varchar (16),
  `chost` varchar (32),
  `cflags` varchar (64),
  `cxxflags` varchar (64),
  `fflags` varchar (64),
  `ldflags` varchar (64),
  `makeopts` varchar (8),
  `lastsync` timestamp null default null,
  `profile` varchar (64),
  `sync` varchar (128),
  primary key (`uuid`),
  foreign key (`uuid`) references `hosts`(`uuid`)
  on delete cascade on update cascade
);

drop table if exists `keywords`;
create table `keywords` (
  `kwkey` serial,
  `keyword` varchar (16),
  primary key (`keyword`)
);

drop table if exists `global_keywords`;
create table `global_keywords` (
  `uuid` binary (16),
  `kwkey` bigint unsigned,
  primary key (`uuid`, `kwkey`),
  foreign key (`uuid`) references `hosts`(`uuid`)
  on delete cascade on update cascade,
  foreign key (`kwkey`) references `keywords`(`kwkey`)
  on delete cascade on update cascade
);

drop table if exists `lang`;
create table `lang` (
  `lkey` serial,
  `lang` varchar (16),
  primary key (`lang`)
);

drop table if exists `host_lang`;
create table `host_lang` (
  `uuid` binary (16),
  `lkey` bigint unsigned,
  primary key (`uuid`, `lkey`),
  foreign key (`uuid`) references `hosts`(`uuid`)
  on delete cascade on update cascade,
  foreign key (`lkey`) references `lang`(`lkey`)
  on delete cascade on update cascade
);

drop table if exists `features`;
create table `features` (
  `fkey` serial,
  `feature` varchar (64),
  primary key (`feature`)
);

drop table if exists `host_features`;
create table `host_features` (
  `uuid` binary (16),
  `fkey` bigint unsigned,
  primary key (`uuid`, `fkey`),
  foreign key (`uuid`) references `hosts`(`uuid`)
  on delete cascade on update cascade,
  foreign key (`fkey`) references `features`(`fkey`)
  on delete cascade on update cascade
);

drop table if exists `gentoo_mirrors`;
create table `gentoo_mirrors` (
  `mkey` serial,
  `mirror` varchar (128),
  primary key (`mirror`)
);

drop table if exists `host_mirrors`;
create table `host_mirrors` (
  `uuid` binary (16),
  `mkey` bigint unsigned,
  primary key (`uuid`, `mkey`),
  foreign key (`uuid`) references `hosts`(`uuid`)
  on delete cascade on update cascade,
  foreign key (`mkey`) references `gentoo_mirrors`(`mkey`)
  on delete cascade on update cascade
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
  `uuid` binary (16),
  `pkey` bigint unsigned,
  `build_time` timestamp null default null,
  `counter` bigint unsigned,
  `kwkey` bigint unsigned,
  `rkey` varchar (64),
  `size` bigint unsigned,
  primary key (`uuid`, `pkey`),
  foreign key (`uuid`) references `hosts`(`uuid`)
  on delete cascade on update cascade,
  foreign key (`pkey`) references `packages`(`pkey`)
  on delete cascade on update cascade,
  foreign key (`kwkey`) references `keywords`(`kwkey`)
  on delete cascade on update cascade,
  foreign key (`rkey`) references `repositories`(`rkey`)
  on delete cascade on update cascade
);

drop table if exists `useflags`;
create table `useflags` (
  `ukey` serial,
  `useflag` varchar (64),
  primary key (`useflag`)
);

drop table if exists `global_useflags`;
create table `global_useflags` (
  `uuid` binary (16),
  `ukey` bigint unsigned,
  primary key (`uuid`, `ukey`),
  foreign key (`uuid`) references `hosts`(`uuid`)
  on delete cascade on update cascade,
  foreign key (`ukey`) references `useflags`(`ukey`)
  on delete cascade on update cascade
);

drop table if exists `plus_useflags`;
create table `plus_useflags` (
  `ipkey` bigint unsigned,
  `ukey` bigint unsigned,
  primary key (`ipkey`, `ukey`),
  foreign key (`ipkey`) references `installed_packages`(`ipkey`)
  on delete cascade on update cascade,
  foreign key (`ukey`) references `useflags`(`ukey`)
  on delete cascade on update cascade
);

drop table if exists `minus_useflags`;
create table `minus_useflags` (
  `ipkey` bigint unsigned,
  `ukey` bigint unsigned,
  primary key (`ipkey`, `ukey`),
  foreign key (`ipkey`) references `installed_packages`(`ipkey`)
  on delete cascade on update cascade,
  foreign key (`ukey`) references `useflags`(`ukey`)
  on delete cascade on update cascade
);

drop table if exists `unset_useflags`;
create table `unset_useflags` (
  `ipkey` bigint unsigned,
  `ukey` bigint unsigned,
  primary key (`ipkey`, `ukey`),
  foreign key (`ipkey`) references `installed_packages`(`ipkey`)
  on delete cascade on update cascade,
  foreign key (`ukey`) references `useflags`(`ukey`)
  on delete cascade on update cascade
);
