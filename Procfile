web: daphne webapps.asgi:application --port $port $PORT --bind 0.0.0.0 -v2
mahjongworker: python3 manage.py runworker --settings=webapps.settings -v2
