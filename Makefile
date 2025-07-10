mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

admin:
	python3 manage.py createsuperuser

loaddata:
	python3 manage.py loaddata apps/fixtures/product.json


dumpdata:
	python3 manage.py dumpdata apps.Product > product.json

translate:
	django-admin makemessages -l uz
	django-admin makemessages -l en
	django-admin makemessages -l ru

compile:
	django-admin compilemessages
