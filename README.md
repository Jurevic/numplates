# Lithuanian number plates REST API

API enables creating car number plates, their owners and cars.

# Run

To start application rename and setup .env-example to .env and run:

    $ docker-compose up --build
    
Browse to [localhost](http://localhost)

# Usage

To create superuser:

    $ docker ps
    $ docker exec -it CONTAINER_ID /bin/sh
    $ source /venv/bin/activate
    $ python3 manage.py createsuperuser

Admin URL is [localhost/admin/](http://localhost/admin/)
    
## API Endpoints

    GET /api/v1/
    GET, POST, PUT, PATCH, DELETE /api/v1/numplates/{:id/}
    GET, POST, PUT, PATCH, DELETE /api/v1/owners/{:id/}
    GET, POST, PUT, PATCH, DELETE /api/v1/cars/{:id/}

## Objects

### Numplate

| Value  | Description                                |
| ------ |:------------------------------------------:|
| id     | Number plate id                            |
| number | Licence plate number string, format AAA000 |
| owner  | Assigned owner id                          |
| car    | Assigned car id                            |

### Car

| Value     | Description                |
| --------- |:--------------------------:|
| id        | Car id                     |
| model     | Car model string           |
| image_url | Car model image url string |

### Owner

| Value      | Description              |
| ---------- |:------------------------:|
| id         | Owners id                |
| first_name | Owners first name string |
| last_name  | Owners last name string  |

# Development

Create and activate virtual environment, install requirements as follows:

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip3 install -r requirements.txt
    
To run standalone:

    $ python3 manage.py runserver

To run tests:

    $ python3 manage.py test
