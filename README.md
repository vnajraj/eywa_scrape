# setup/run

1. git clone ...
2. create .env 
```
 export EYWA_HOST="http://..."
 export EYWA_USER="..."
 export EYWA_PASSWORD="..."
```
3. source .env
4. load dataset into eywa and deploy
5. make test


# data model

![data model](https://github.com/vnajraj/eywa_scrape/blob/master/images/dataset.png)

# what's used

1. requests-html for web scraping
2. requests for fetching token
3. graphqlclient for loading data into eywa


# misc

## run db
```
docker run --name eywa -p 5432:5432 -e POSTGRES_PASSWORD=password --rm postgres
```
## setup eywa
```
alias e=eywa
e core environment -s local
e core version -s 0.1.4
e core init
e core super -s admin
e core start
e core gen-config
e env

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## other
```
e core version -l
```
## running commands
```
e run -c "python load.py"
```
