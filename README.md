# library-inventory

### Steps to get up and running
1. Ensure you're in the root of the project directory
2. `docker build -t library-inventory-api:latest .`
3. `docker-compose -f stack.yml up`

### Stopping the services
In order to start over with a fresh data model, run:

`docker-compose -f stack.yml down -v`


### To-Dos
1. Handle race conditions / stale data
2. Update integration / smoke tests and add unit tests
3. Update docstrings
4. Black formatter / PyLint

### Extensions
1. Auth / changing displayed data based on logged in user
2. Refactor to reduce duplication in boilerplate
3. Configuration files and/or command line arguments
4. DB indexing
5. Implement or list convenience endpoints 
