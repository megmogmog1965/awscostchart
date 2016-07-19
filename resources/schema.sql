
/* AWS ACCESS KEY一覧 */
create table if not exists accesskeys (
  aws_access_key_id text primary key not null,
  aws_secret_access_key text not null,
  name text not null
);
