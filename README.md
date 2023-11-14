## Running  and using the tool:
Ensure that port 27017 is free on your machine (mongo instance will use this port). \
Open a terminal in the project's root directory and do the following:
#### - Start the Url shortener app by running:
```
$ docker compose up -d
```
#### - When the app is up and running, run the command:
```
$ docker exec -it url_shortener_tool bash
```
With the above command we opened a bash shell in the app's docker container and we will 
run commands in the container's shell.
#### - Test the tool by running the following commands in the container's shell that we opened above:
```
$ python main.py --minify 'https://www.linkedin.com/jobs/search/?cur&rentJobId=368wrhfrsds'
$ python main.py --expand 'camarasoft.com/gsiKna'
```
Make sure that you enter the urls in single quotes otherwise the shell will remove some characters from 
the url and then send it incorrectly to the python program.

The expiration time of the urls is currently set for 20 seconds for testing reasons.
You can change it from the app/main.py file. You can change it while the program is up and running as well.

## Running the tests:
Ensure you have installed all the test libraries imported in tests/test_url_shortener.py: \
Open a new terminal in the project's root directory and run:
```
$ pytest
```
I only implemented few of the tests that need to be implemented.