# Flask Crypto API

## Features
- JWT-based Auth
- Coin listing, categories, filter by ID
- Paginated responses
- Swagger docs
- Unit testing with pytest

## Setup

```bash
pip install -r requirements.txt
python run.py
```

## Auth

POST `/login`  
```json
{ "username": "", "password": "" }
Look the credentials.py for credentials.
```

Use token as:  
`Authorization: Bearer <token>`

## API

- `/coins`
- `/categories`
- `/filtered-coins`

## Test

```bash
pytest test_routes.py
```
