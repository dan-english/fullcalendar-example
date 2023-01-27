# fullcalendar-nylas


## Project Setup

```shell script
npm install
```

### Compile and Hot-Reload for Development
(if using the NPM server)
```shell script
npm run dev
```

### Compile and Minify for Production
(if using the Flask server)
```shell script
npm run build
```

### Start Flask Server
```shell script
. venv/bin/activate
pip install -r requirements.txt
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

The VueJS front end can be started by running `npm run dev` this will initialise its own server and port.

The Python logic can be started bu running `flask run` this will also initalise its own server and port.

### Note:
If changes are not picked up then stop/start the Flask server as it does not pick up the new compiled assets.
Also, if using the Flask server then you will need to run `npm run build` as the Flask config is pointing at production assets.
