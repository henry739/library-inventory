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
3. Provide API specification

### Extensions
1. Auth / changing displayed data based on logged in user
2. Refactor to reduce duplication in boilerplate.
   - users controllers and books controllers are almost identical
   - loans controllers contains special logic
3. Configuration files and/or command line arguments
4. DB indexing
5. Implement or list convenience endpoints 
