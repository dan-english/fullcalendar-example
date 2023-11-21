# fullcalendar-nylas

This project should be considered WIP and not to be consumed in a production environment without thorough testing.
It's purpose is to provide an example of availability data from Nylas and Full Calendar IO.



## Project Setup

```shell script
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
npm install
npm run build
cp .env.example .env
### update the environment file with your token(s)
flask run
```

## Python Packages
- flask (https://flask.palletsprojects.com/en/2.2.x/)
- flask-cors
- requests
- python-dotenv


## FullCalendar Library
```
https://fullcalendar.io/
```


### Note:
If build changes are not picked up then stop/start the Flask server.
