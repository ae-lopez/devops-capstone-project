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