mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

admin:
	python3 manage.py createsuperuser

loaddata:
	python3 manage.py loaddata apps/fixtures/product.json


dumpdata:
	python3 manage.py dumpdata apps.Category > category.json
