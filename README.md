# URL Shortener

URL Shortener is an open source mini service which does exactly what it is meant to - makes urls shorter.

## How It Works
URL Shortener consists of API and [Redis](https://redis.io/) database.
* API receives url addresses that will be shortened and redirects users
* Database contains all urls

Now the project works only with Redis database, maybe there will be more...

## Installation
The only way to install URL Shortener is to download it. No any packages at PyPi :(  
### Reids
Also, you have to install [Redis](https://redis.io/) on the machine which will perform redirections. I suggest you install Redis following the [instruction](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04) for Ubuntu. 

### Run Server
* Install all dependencies
``` bash
pip install -r requirements.txt
```
* Edit database settings in config file (only default settings available now, so skip this)
* Run the server
``` bash
uvicorn main:app --host 0.0.0.0 --port <your_port> --workers <num_workers>
```
Thats it, server is up and running. 

## Usage
You can check a very pretty documentation for api at <your_ip>:<your_port>/docs.

The service works with only 2 types of requests now:
* **Post** request to put your url into database and return shortened varian
* **Get** request to redirect users who open shortened urls

Further improvements and additional functions are coming soon. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)