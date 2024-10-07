# Create a docker image:
Use the docker build command to build a Docker image called accounts from the Dockerfile.

`docker build -t accounts .`

Use the docker run command to test that your image works properly. The PostgreSQL database is running in a Docker container named postgres so you will need to --link postgres and set the environment variable DATABASE_URI to point to it. You might also want to use the --rm flag to remove the container when it exists

```
docker run --rm \
    --link postgresql \
    -p 8080:8080 \
    -e DATABASE_URI=postgresql://postgres:postgres@postgresql:5432/postgres \
    accounts
```

# Run the rest service
1. Refresh database: `flask db-create`
2. start service w new database: `make run` 

## demo create an account 
```
curl -i -X POST http://127.0.0.1:5000/accounts \
-H "Content-Type: application/json" \
-d '{"name":"John Doe","email":"john@doe.com","address":"123 Main St.","phone_number":"555-1212"}'
```

## demo list all accounts
```
curl -i -X GET http://127.0.0.1:5000/accounts
```

## demo read an account
```
curl -i -X GET http://127.0.0.1:5000/accounts/1
```

## demo update an account
```
curl -i -X PUT http://127.0.0.1:5000/accounts/1 \
-H "Content-Type: application/json" \
-d '{"name":"John Doe","email":"john@doe.com","address":"123 Main St.","phone_number":"555-1111"}'
```

## demo delete an account
```
curl -i -X DELETE http://127.0.0.1:5000/accounts/1
```