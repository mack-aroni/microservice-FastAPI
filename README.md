# microservice-FastAPI
Microservice project using a FastAPI Python backend with a NodeJS frontend app.

# Build
To build, have docker desktop installed and use:
```
docker-compose up --build"
```
The pod will then run and you can access the frontend app on "localhost:3000".

# .env File
You also must create a .env file in the same directory as the docker-compose.yml with the format: <br />
```
# Redis DB for Inventory microservice
REDIS_INV_HOST= <hostname>
REDIS_INV_PORT= <port>
REDIS_INV_PASSWORD= <password>

# Redis DB for Payment microservice
REDIS_PAY_HOST= <hostname>
REDIS_PAY_PORT= <port>
REDIS_PAY_PASSWORD= <password>
```
As part of the microservice format the two redis DBs should be two separate DBs.
