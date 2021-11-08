# Auth0 authorization & authentication flows

This repo shows the implementation of the different Auth0 flows both for authenticate and authorize a user both at web app level and hitting a protected API endpoint

## Run
Every flow implementation has its own start script
```shell
sh start.sh
```

One thing is getting access to the site through Auth0 either using a social account or connection to own DB  and another thing is hitting own APIs Auth0 protected.
In order to get access to a site do this using a Google Account through Auth0:

1. Create an Auth0 account
2. Create a tenant. A tenant is a logically isolated group of users who share common access requirements with specific privileges (https://auth0.com/docs/get-started)
3. Go to dashboard > Applications > Application > Create Application. Choose Regular Web Application
![Applications in Auth0 menu](images/menu.png)
4. Assign a name to the App. `My app`for name and Regular Web applications were the values chosen for this repository. 
![Applications in Auth0 menu](images/create_app.png)
5. In the next screen choose a language to develop the integration with the application
6. In order to access to Auth0, a `CLIENTID` (AUTH0_CLIENT_ID) & `CLIENTSECRET` (AUTH0_CLIENT_SECRET) should be provided. Also, the `Domain` (AUTH0_DOMAIN) can be found in the `Settings` tab.
7. `Allowed Callback URL` includes an endpoint in the application that is going to authorise the access and return user's information.
8. `Allowed Logouts URLs` is the URL where the user will go once logged out.
9. For both URLs the https protocol should be used. http protocol will produce a payload error. So, the script will create a self-signed certificate for localhost

## Create API Applications

This type of applications are used to get tokens to do authentication/authorization for our own APIs. 
Normally these tokens travel in the header of the request using `Autorization` as a `Bearer token`. Example:
```json
"headers" : {
  'Authorization': 'Bearer ea234234.adasda.asdasd'
}
```

1. To create an API, go to Applications > API > Create API
![API in Auth0 menu](images/create_api.png)
2. Assign a name, an identifier (a non-public URL of the API) 
3. Go to Test and discover the `client_id` (AUTH0_API_CLIENT_ID), `secret_id` (AUTH0_API_CLIENT_SECRET)

## Notes:

The env variable `FLASK_APP=app.py` indicates the file that contains the flask application. If this env variable is set the command to run the application is `flask run --reload` (for development). If this variable is not passed through the way to run the application is with `python app.py -h 0.0.0.0`.
The outcome should be: `Oh happy day!`

## TODO

Update the code according to this: https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https