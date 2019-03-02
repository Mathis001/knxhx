# Knxhx

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 6.0.3.

## Requirements

- Install Python3, Python3 pip (pip3), Angular, and MySQL.

    - On Ubuntu 18.04:
    - `sudo apt install apache2 python3 python3-pip python3-mysqldb mysql-server npm`
    - `sudo npm install -g @angular/cli@6.0.3`

- `git clone https://github.com/Mathis001/knxhx`

- Change directories to the root folder of the project: `knhx/`

- Run `sudo pip3 install -r python/requirements.txt --user` to install python dependancies.

## Initialize

- To create the database schema, run `sudo mysql < database/db_schema.sql`

## Run server

- Run `ng serve  --watch --host=<address> --port=4200` to launch Angular service. The app will automatically reload if you change any of the source files.

- Change directory to `python/` and run `sudo python3 server.py` for the Python Flask API.

- Navigate to `http://<address>:4200/` for the web interface and `http://<address>:5000/api/v1/ui/` for the api documentation.

- To give yourself admin access, create a cookie in your browser for the server with the name `auth_pubtkt` and value `uid%3Dadmin`. You can also replace "admin" with any created users to help test permission and departments.
## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
