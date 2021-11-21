# Auth0 authorization permissions implementation 

This repo demonstrates the working permissions already set up in Auth0 for two different protected endpoints  

## Run
Every flow implementation has its own start script
```shell
sh start.sh
```

## Protected endpoints

The protected endpoints are:

Admin role ->  for_admins()
Readers roles -> for_readers()

## Important

The permissions for the API in Auth0 are assigned to the whole application not to every endpoint. 
The permissions per se are set in the decorator of the respective protected endpoint.
For example:
- The permission `get:greetings_for_admins` is assigned to the role `admin` and set for the endpoint `def for_admins()`
- The permission `get:greetings_for_guests` is assgined to the role `guests` and set for the endpoint `def for_guests(`

## TODO

Update the code according to this: https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https