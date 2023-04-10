# Melon Back-end

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Melon is a Python messenger API

## Install and Run
To install Melon:

```shell
$ git clone git@github.com:Smbrer1/melon-back-end.git
$ cd melon-back-end
$ pip install -r requirements.txt
```

To run Melon:
```shell
$ uvicorn back_end.main:app
```

## Configuration
To configure this API you need to create .env file with this structure
```text
JWT_SECRET_KEY = <secret key here>
JWT_REFRESH_SECRET_KEY = <secret key here>
MONGO_CONNECTION_STRING = mongodb://host:port
```

## Docs
If you run this app without specified host, full openApi docs will be here:
http://127.0.0.1:8000/docs