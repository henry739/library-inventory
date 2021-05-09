# library-inventory

## Operations v1
### Books API
* `POST /api/v1/books`
* `DELETE /api/v1/books/{id}`
* `GET /api/v1/books?title={}` - Rationale for this being a GET: You could bookmark popular searches.
* `GET /api/v1/books/{id}`
  
### Users API
* `POST /api/v1/users`
* `GET /api/v1/users?name={}`
* `GET /api/v1/users/{id}`
* `PUT /api/v1/users/{id}`

### Loans API
* `POST /api/v1/loans`
* `GET /api/v1/loans/{id}`
* `DELETE /api/v1/loans/{id}`
  
What happens when you delete a book or user involved in a loan? Perhaps we need to delete the loan first?
