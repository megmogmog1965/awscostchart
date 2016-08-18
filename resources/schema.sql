
/* AWS ACCESS KEY一覧 */
create table if not exists awskeys (
  aws_access_key_id text primary key not null,
  aws_secret_access_key text not null,
  name text not null
);

/* AWS ACCESS KEY一覧 */
create table if not exists service_costs (
  id integer primary key not null,
  service_name text not null,
  aws_access_key_id text not null,
  timestamp integer not null,
  value real not null
);
