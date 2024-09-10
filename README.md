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

# Backend Breakdown
The two independant microservices, payment and inventory, utilize the redis ORMs and allow communication through REST stlye API calls. <br />
They both provide CRUD style operations for use through the frontend interface and also include a simulated payment pipeline with <br />
initial checking, payment submitting, allowing for processing time, and payment confirmation or refunding.
