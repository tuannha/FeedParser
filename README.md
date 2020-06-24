# DJANGO FEED READER

## PREPARE FOR ENVIRONMENT

* export python path

```shell script
export PYTHONPATH='$PYTHONPATH:./'
```

* For production

```shell script
pip install -r requirements.txt
```

* For developers

```shell script
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

Enable commit hook to test the project before committing 

```shell script
cd .git/hooks
ln -s ../../hooks/pre-commit .
```

## FIRST RUN 

* Migrate database

```shell script
./manage.py migrate
```

* Create superuser

```shell script
./manage.py createsuperuser
```

* Start service 

```shell script
./manage.py runserver
```

* Visit the website at [http://localhost:8000](http://localhost:8000) 

## FETCH DATA

```shell script
./manage.py fetch_article --sources=<YOUR RSS URLS, SEPARATED BY COMMA>
```