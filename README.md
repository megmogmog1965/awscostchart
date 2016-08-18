# awscostchart

## Usage

Setup.

```
# clone repos.
git clone https://github.com/megmogmog1965/awscostchart.git

# build project.
cd awscostchart
pip install flask flask-autodoc boto
npm install
npm run build

# start server.
npm run start

# register your aws account to server.
curl -XPOST -H 'Content-type: application/json' -d '
{
  "aws_access_key_id": "YOUR AWS ACCESS KEY ID",
  "aws_secret_access_key": "YOUR AWS SECRET KEY",
  "name": "DISPLAY NAME"
}' http://localhost:5001/apis/awskeys
```

Access charts.

* http://localhost:5001/

See apis.

* http://localhost:5001/apis/

## Author

* Yusuke Kawatsu


[Yusuke Kawatsu]:https://github.com/megmogmog1965
