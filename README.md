# cycraft-backend
A restaurant review system with only backend APIs.

## Getting Started

### Environment
- linux
- python3.10
- docker

### Installation
1. Create virtual environment
    ```bash
    python3.10 -m venv env
    ```
2. Run postgres docker container
    ```bash
    docker run -d --name local-postgres -e POSTGRES_USER=... -e POSTGRES_PASSWORD=... -e POSTGRES_DB=... postgres
    ```
3. Create a `.env` file by referencing `.env.example`
4. Activate virtual environment
    ```bash
    . env/bin/activate
    ```
    You should see `(env)` at the beginning of your terminal prompt
5. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
6. Make migrations and migate
    ```bash
    python gastronome/manage.py makemigrations
    python gastronome/manage.py migrate
    ```
7. (Optional) Create superuser to access admin page
    ```bash
    python gastronome/manage.py createsuperuser
    ```

### Start Application
1. Start postgres docker container
    ```bash
    docker start local-postgres
    ```
2. Start server
    ```bash
    ./start_server.sh
    ```

### Testing
1. Start postgres docker container (if not running)
    ```bash
    docker start local-postgres
    ```
2. Run tests
    ```bash
    ./test.sh
    ```

## Features / API Documentation

### Authentication API Endpoints

#### POST /api/token/
Get JWT token

**Request Body**
```json
{
    "username": "jean",
    "password": "password"
}
```

**Response**
- status: 200
```json
{
    "access": "...",
    "refresh": "..."
}
```

#### POST /api/token/refresh/
Refresh JWT token

**Request**
```json
{
    "refresh": "..."
}
```

**Response**
- status: 200
```json
{
    "access": "..."
}
```

### Restaurant API Endpoints

#### POST /api/restaurants/
Create restaurant
> Only user with `is_business=True` can create restaurant

**Request**
- Header: `Authorization: Bearer ...`
```json
{
    "name": "restaurant name",
    "description": "restaurant description",
    "address": "restaurant address"
}
```

**Response**
- status: 201
```json
{
    "id": "...",
    "rating": null,
    "total_reviews": 0,
    "name": "restaurant name",
    "description": "restaurant description",
    "address": "restaurant address",
    "created_at": "2024-06-03T13:13:29.699518Z",
    "updated_at": "2024-06-03T13:13:29.699584Z",
    "created_by": "..."
}
```

#### GET /api/restaurants/
Get restaurants

**Query Params**
- ordering:
    - `rating`: order by rating descending
    - `rating`: order by rating ascending

**Request**
- Header: `Authorization: Bearer ...`

**Response**
- status: 200
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "...",
            "rating": null,
            "total_reviews": 0,
            "name": "restaurant name",
            "description": "restaurant description",
            "address": "restaurant address",
            "created_at": "2024-06-03T13:13:29.699518Z",
            "updated_at": "2024-06-03T13:13:29.699584Z",
            "created_by": "..."
        }
    ]
}
```

#### PATCH /api/restaurants/{id}/
Update restaurant
> Only the restaurant owner (the user who created it) can update that restaurant.

**Request**
- Header: `Authorization: Bearer ...`
```json
{
    "name": "restaurant name update",
    "description": "restaurant description update",
    "address": "restaurant address update"
}
```

**Response**
- status: 200
```json
{
    "id": "...",
    "rating": null,
    "total_reviews": 0,
    "name": "restaurant name update",
    "description": "restaurant description update",
    "address": "restaurant address update",
    "created_at": "2024-06-03T13:13:29.699518Z",
    "updated_at": "2024-06-03T13:20:21.904802Z",
    "created_by": "..."
}
```

#### DELETE /api/restaurants/{id}/
Delete restaurant
> Only the restaurant owner (the user who created it) can delete that restaurant.

**Request**
- Header: `Authorization: Bearer ...`

**Response**
- status: 204

### Review API Endpoints

#### POST /api/reviews/
Create review
> Only user with `is_business=False` can create review

**Request**
- Header: `Authorization: Bearer ...`
> The score can only be an integer, with a range from 1 to 5
```json
{
    "restaurant": "...",
    "score": 3,
    "comment": "review comment"
}
```

**Response**
- status: 201
```json
{
    "id": "...",
    "score": 3,
    "comment": "review comment",
    "created_at": "2024-06-03T13:29:03.738182Z",
    "updated_at": "2024-06-03T13:29:03.738194Z",
    "restaurant": "...",
    "created_by": "..."
}
```

#### GET /api/reviews/?restaurant={id}
Get reviews

**Query Params**
> You must provide one of the query params
- restaurant: id of certain restaurant
- user: id of certain user

**Request**
- Header: `Authorization: Bearer ...`

**Response**
- status: 200
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "...",
            "score": 3,
            "comment": "review comment",
            "created_at": "2024-06-03T13:29:03.738182Z",
            "updated_at": "2024-06-03T13:29:03.738194Z",
            "restaurant": "...",
            "created_by": "..."
        }
    ]
}
```

#### PATCH /api/reviews/{id}/
Update review
> Only the review owner (the user who created it) can update that review.

> The restaurant cannot be updated

**Request**
- Header: `Authorization: Bearer ...`
```json
{
    "score": 5,
    "comment": "review comment update"
}
```

**Response**
- status: 200
```json
{
    "id": "...",
    "score": 5,
    "comment": "review comment update",
    "created_at": "2024-06-03T13:29:03.738182Z",
    "updated_at": "2024-06-03T13:38:24.684329Z",
    "restaurant": "...",
    "created_by": "..."
}
```
#### DELETE /api/reviews/{id}/
Delete review
> Only the review owner (the user who created it) can delete that review.

**Request**
- Header: `Authorization: Bearer ...`

**Response**
- status: 204
