# Photo Gallery
## Overview
It consists of a backend application that allows the client to register images in an album and gives permissions to the user.
Only users registered for a certain album can register images and comment on the images in the album.
The album owner has a buddy or companion who can also add users with permissions.

Album images will be stored on S3.

## Installation Instructions


### Installation

Pull down the source code from this GitLab repository:

```sh
$ gh repo clone GiovaniGitHub/photos-gallery
```

```sh
$ cd photos-gallery
$ python3 -m venv env
```

Activate the virtual environment:

```sh
$ source venv/bin/activate
```

Install the python packages specified in requirements.txt:

```sh
(venv) $ pip3 install -r requirements.txt
```

### Config 

Choice a env , ```.env.dev.template``` or ```.env.prod.template```, and create a file ```.env.dev``` or ```.env.prod.template```, and set values of environment variables.

Create a new virtual environment.


### Docker Compose

Download, build and create containers
```sh
docker-compose build
```

Run Docker containers
```sh
docker-compose up
```

### Testing

```sh
(venv) $ cd services/api
(venv) $ pytest -c pytest.ini
```

Navigate to 'http://localhost:5000' in your favorite web browser to view the website!

## Key Python Modules Used

* **Flask**: micro-framework for web application development which includes the following dependencies:
* **Flask-Restful**: Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs.
* **pytest**: framework for testing Python projects
* **Flask-SQLAlchemy** - ORM (Object Relational Mapper) for Flask
* **Flask-Login** - support for user management (login/logout) in Flask
* **Flask-WTF** - simplifies forms in Flask
* **Flake8** - static analysis tool
* **Boto3** - lib/client to use and connect to AWS S3.
* **Marshmallow** -  ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes.

This application is written using Python 3.10.
