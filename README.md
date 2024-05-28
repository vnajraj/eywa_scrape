# execution environment

Refactored to start using eywa_client library for comms with EYWA - JSONRPC
over stdout.

To start the script one should run:

```
e run -e local -c "make run"
```

Note: the robot definition expects input data:
```
"scrapeHours" = {
    "start" : 0
    "stop" : 23
}
```

# setup/run

1. load dataset into eywa and deploy
2. add git repo to eywa using eywa-client branch
3. add the robot
4. launch the robot (define both stop and start hours - 0-23)

# data model

![data model](https://github.com/vnajraj/eywa_scrape/blob/master/images/dataset.png)

# what's used

1. requests-html for web scraping
2. eywa_client for comms with eywa

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
```
## other
```
e core config-path
e core config-schema
e core version -l
```
## running commands
```
e run -e local -c "source venv/bin/activate" -c "python scrape.py"
```
