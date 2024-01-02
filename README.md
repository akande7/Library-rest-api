# Introduction

This API contains basic features for a scalable library platform. It includes endpoints to add, delete and search for books, and view various genres and authors.

## About the Stack

The API follows the REST pattern. It is built with python and flask, a lightweight backend microservices framework required to handle requests and responses, and uses flask-CORS to handle cross-origin requests.

## Documentation Example

1. `GET \\books?page=<page_number>`
Fetches all books of all available genres paginated
Requestameters (optional): page:int

Example response:
```json
 
 "books": [
   {
      "name": "Think like a monk", 
      "genre": "Self-development", 
      "rating": 9.5, 
      "author": "Jay Shetty", 
    }, 
    {
      "name": "The Doomsday Conspiracy", 
      "genre": "fiction", 
      "rating": 7.5, 
      "author": "Sidney Sheldon", 
    }, 
 ], 
 "success": true, 
 "total_books": 2
 "genres": {
  "1": "comedy",
  "2": "thriller",
  "3": "romance",
  "4": "History",
  "5": "crime fiction",
  "6": "Sports"
}
```


2. `GET '/authors'`
Fetches a dictionary of authors in which the keys are the ids and the value is the corresponding string of the author
Request Arguments: None
Returns: An object with a single key, `author`, that contains an object of `id: author_string` key: value pairs.

Example response:

```json
"success": true, 
"total_authors": 4
"authors":
{
  "1": "Jay Shetty",
  "2": "Sidney Sheldon",
  "3": "Simon Kernick",
  "4": "Gandhi",
}
```

 
3.`GET '/genres'`
Fetches a dictionary of genre in which the keys are the ids and the value is the corresponding string of the genre
Request Arguments: None
Returns: An object with a single key, `genre`, that contains an object of `id: genre_string` key: value pairs.

Example response:

```json
{
  "1": "comedy",
  "2": "thriller",
  "3": "romance",
  "4": "History",
  "5": "crime fiction",
  "6": "Sports"
}
```

4.`DELETE /books/<book_id>`
Delete an existing book specified by user with book_id from all available books 
Request arguments: book_id:int

Example response:
```json
{
  "deleted": "11", 
  "success": true
}
```

5.`POST /books`
Add a new book to the available books
Request body: {name:string, genre:string, rating:int, author:string}

Example response:
```json
{
  "created": 20, 
  "success": true
}
```

6.`POST /books/search`
Fetches all books where a substring matches the search term (not case-sensitive)
Request body: {searchTerm:string}

Example response:
```json
{
   
  "success": true,
  "books": [
    {
      "name": "Think like a monk", 
      "genre": "Self-development", 
      "rating": 9.5, 
      "author": "Jay Shetty", 
    }
  ], 
  "total_books": 1,
  "current_genre": null,
}
```

7.`GET /genre/<int:id>/books`
Fetches books for the specified genre specified by user with genre_id
Request argument: id:int
```json
Example response:
{
  "success": true, 
  "books": [
    {
      "name": "Think like a monk", 
      "genre": "Self-development", 
      "rating": 9.5, 
      "author": "Jay Shetty", 
    }, 
    {
      "name": "Think Big", 
      "genre": "Self-development", 
      "rating": 7.5, 
      "author": "John Stevens", 
    }, 
  ], 
   
  "total_books": 2,
  "genre": "Self-development"
}
```
8.`GET /authors/<int:id>/books`
Fetches books for the specified author specified by user with author_id
Request argument: id:int
```json
Example response:
{
  "success": true, 
  "books": [
    {
      "name": "Think like a monk", 
      "genre": "Self-development", 
      "rating": 9.5, 
      "author": "Jay Shetty", 
    }, 
    {
      "name": "8 rules of love", 
      "genre": "Romance", 
      "rating": 7.5, 
      "author": "Jay Shetty", 
    }, 
  ], 
   
  "total_books": 2,
  "author": "Jay Shetty"
}
```
 
