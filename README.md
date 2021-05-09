# library-inventory

### Steps to get up and running
1. Ensure you're in the root of the project directory
2. `docker build -t library-inventory-api:latest .`
3. `docker-compose -f stack.yml up`

### Stopping the services
In order to start over with a fresh data model, run:

`docker-compose -f stack.yml down -v`


### To-Dos & Extensions
1. Handle race conditions / stale data
2. ~~Prevent deletion of books if active loans use them~~
3. Update integration / smoke tests and add unit tests
4. ~~Integrate with external PostgreSQL service~~
5. Update docstrings / consider using open-api annotations / update README
6. Auth / changing displayed data based on logged in user
7. Implement or list convenience endpoints 
8. Refactor to reduce duplication in boilerplate
9. Black formatter / PyLint
10. DB indexing
11. Configuration files and/or command line arguments
