# World Timezone API

This API is used to get worldwide timezones from a list of selected cities, by connecting to the http://worldtimeapi.org API.
## Installation

In terminal, in the root folder of the app, install all the libraries listed in the Requirements.txt file:
```bash
pip install -r requirements.txt
```
install
```pip install virtualenv [--user]```

###Creating a Virtual Enviroment
create an environment in the root path of the project
```
python3 -m venv [/path/to/new/virtual/environment]
```
Activate the new virtual environment
```
source [venv path]/bin/activate
```

Then Run the app:
```bash
python main.py
```

## Usage

In the browser, go to:
```python
localhost:4240/times
```

it will output a JSON response like this:
```python
{
    "Africa/Accra": "2022-07-29T12:36:29.855235+00:00", 
    "America/Belize": "2022-07-29T12:36:29.916750+00:00", 
    "Antarctica/Davis": "2022-07-29T12:36:29.991832+00:00", 
    "Asia/Baghdad": "2022-07-29T12:36:30.064340+00:00", 
    "Australia/Eucla": "2022-07-29T12:36:30.137697+00:00", 
    "Europe/Zurich": "2022-07-29T12:36:30.268828+00:00"
 }
```

To get just one city, go to:
```
localhost:4240/times/city/[Continent Name]/[City Name]]
```

For example:
```
localhost:4240/times/city/America/Belize
```

it will output a JSON response like this:
```python
{
    "America/Belize": "2022-07-29T12:36:29.916750+00:00", 
 }
```


## Docker
Just execute the Docker Compose command:
```
docker-compose up -d
```
It will create three containers:
<li><b>redis</b> on port localhost:6379</li>
<li><b>redisinsight</b> on port localhost:8081</li>
<li><b>web</b> on port localhost:4242</li>

Then you can just go to:
```
http://localhost/4242/times
```

To retrieve the multiple timezones.

#Testing

Run the file testTimes
```
python testTimes.py
```

It will run two tests, one to check the Redis connection and another to check whether a request to the World Time API can be established.