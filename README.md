# library-inventory

### Steps to get up and running
1. Ensure you're in the root of the project directory
2. `docker build -t library-inventory-api:latest .`
3. `docker-compose -f stack.yml up`

### Stopping the services
In order to start over with a fresh data model, run:
1. `docker-compose -f stack.yml down -v`
2. `docker-compose -f stack.yml up`


### API Documentation
#### Registered Users
- `POST /api/v1/users` 
  - Allows any librarian to add a new user to the system
- `GET /api/v1/users?full_name={full_name}` 
  - Allows any librarian to search amongst registered users by full name, returning a list
  - Each user object returned contains a list of active loans for that user
- `GET /api/v1/users/{id}` 
  - Allows any librarian to find a user by id
  - Each user object returned contains a list of active loans for that user
- `DELETE /api/v1/users{id}` 
  - Allows any librarian to delete a user by id
  - Disallowed if book is part of an active loan

#### Book Inventory
- `POST /api/v1/books` 
  - Allows a senior librarian to add a new book to the inventory
- `GET /api/v1/books?title={title}` 
  - Allows any librarian to search amongst books in the inventory by title, returning a list
  - Each book object contains a list of active loans it is a part of. Since there may be many copies, and different
    books with the same title, this allows the librarian to select a specific copy, and use its id to create the 
    loan.
  - [ ] TODO: Restrict viewing of user ID associated with the loan to senior librarians
- `GET /api/v1/books/{id}`
  - Allows any librarian to search for a specific copy of a book by id
  - Each book object contains a list of active loans it is a part of (0 or 1)
  - [ ] TODO: Restrict viewing of user ID associated with the loan to senior librarians
- `DELETE /api/v1/books/{id}`
  - Allows a senior librarian to delete a book from the inventory by id
  - Disallowed if book is part of an active loan

#### Loans
- `POST /api/v1/loans`
  - Allows any librarian to check out a book for a user, by creating a "Loan" between a user, and a copy of a book
  - The due date is generated, based on "library policy", which is currently set to 7 days in the future
  - A user cannot borrow a copy of a book if:
    - They have 4 or more active loans
    - The book copy is on loan
- `GET /api/v1/loans/{id}`
  - Allows any librarian to search for a specific loan by id
  - This is here for completeness, as a web front-end may require this behaviour
- `DELETE /api/v1/loans/{id}`
  - Allows any librarian to delete a loan from the system by id 
  
#### Login
- `POST /api/v1/login`
  - Allows any librarian to authenticate to the system
  - Response by returning a Json Web Token, signed by the server
  - This JWT must be supplied with each subsequent request
    

### Illustrative Use-Case
1. Alice goes to the library, and sits down in front of the librarian. Barry, a librarian, logs into the system.
   - `POST /api/v1/login`
2. Barry searches the system using Alice's full name, to see if she has registered.
   - `GET /api/v1/users?full_name=Alice`
   - Returns an empty array. She isn't registered yet.
3. Barry registers Alice in the system
   - `POST /api/v1/users`
   - Returns her user id, which Barry takes a note of.
4. Barry searches for 1984 in the system
   - `GET /api/v1/books?title=1984`
   - Returns a list containing 3 copies of the book. Two have loans associated with them, but one doesn't! Barry notes
    the book id.
5. Barry creates a new loan of this copy of 1984 to Alice
   - `POST /api/v1/loans`
6. Agatha, a senior librarian, logs into the system
   - `POST /api/v1/login`
7. Agatha checks today's order, and sees that two copies of Animal Farm have arrived. She adds them to the inventory.
   - `POST /api/v1/books`
   - `POST /api/v1/books`
   - The returned IDs are used to generate a barcode / label to affix to the book.
8. Bob, a frequent user of the library, walks up to Agatha and asks to check in a copy of 1984 he has on loan. He has
   his user id handy. Each book in the library has its ID printed on a label inside the book. Agatha brings up Bob's 
   info
   - `GET /api/v1/users/< bob's user id >`
   - Returns Bob's user info, and the list of his active loans.
   - Agatha selects the loan matching the book id
9. Agatha "checks in" the book by deleting the loan from the system
    - `DELETE /api/v1/loans/< bob's loan of 1984 id >`

### To-Dos
1. Improve unit test coverage
2. Handle senior librarian route in book searches

### Future Work 
1. Refactor to reduce duplication in boilerplate code
2. Source connection parameters from environment variables
3. Enhance search functionality for books, and provide other convenience endpoints
4. Indexing the database to improve performance under a high volume of data
5. Allow updating of users in the system, using the PUT verb
6. Add user registration to the system
7. Enhance authentication features, such as adding a /logout endpoint and hashing the password using `bcrypt`.
8. Swagger documentation
