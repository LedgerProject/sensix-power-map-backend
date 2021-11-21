Sensix PowerMap Backend
===

### Intro 

This is the PowerMap backend to anonymize and aggregate power quality metrics.

Our mission is to automate electric energy audits with our analytics platform so that our clients can better maintain their electric grid and reduce energy costs by 30%.
All this while using energy responsibly and reducing climate change impact.

By providing affordable and open power quality measurement equipment, we hope to increase adoption also among households - choosing a freemium community account from [Sensix](https://sensix.io/). You benefit from accurate and permanent electric power tracking. In exchange, you contribute to an open, anonymized, and aggregated power quality map so that people can spot electric grid issues and held utilities responsible for keeping an optimal infrastructure for everybody to use.

### Run it locally

This project is using [Django](https://www.djangoproject.com/) and [Django Rest Framework](https://www.django-rest-framework.org/).

In production, we use a PostgresDB instance, but to run it locally, a `sqlite3` db is used by default. 

Clone this repo, create a python3 `virtualenv`.

Activate the virtualenv and run `runserver` to see a Django admin interface.

Edit `settings/integrations/mqtt.py` to connect to your MQTT broker, then run the Django command that connects and subscribes to those topics,
so that it aggregates all incoming device payloads into `geohash` areas.

```
./manage.py subscribe_to_processed_payloads
```

### Run tests

```
./manage.py test --settings=project.settings.tests.dev
```


