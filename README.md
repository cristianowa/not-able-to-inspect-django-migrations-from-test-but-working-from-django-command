# Django migrations checker

Repository created to demonstrate [this stack overflow question](https://stackoverflow.com/questions/69319240/not-able-to-inspect-django-migrations-from-test-but-working-from-django-command)

This migrations were created in "parallel", simulating the creation in two branches

```
sampleapp/migrations/0002_samplemodel_leaf1.py
sampleapp/migrations/0002_samplemodel_leaf2.py
```

The command
```
pytest --no-migrations
```
PS: the whole point of this is to be able to detect migration errors without running them

Don't trigger/find an error, while running this command does:
```
python manage.py check_migrations
```