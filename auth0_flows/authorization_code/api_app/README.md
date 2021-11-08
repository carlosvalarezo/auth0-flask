This repo shows how to implement authorization code flow.

1. It loggins to my app using auth0 login page
2. It asks for permissions to see the Google profile (since I am using Google to authenticate)
3. If the authentication is successful, Auth0 redirects the user to my app dashboard
4. Behind the scenes my app receives a code (as a result of the login with Google) that exchanges for a token to get access to a protected endpoint in my app
5. Using the token it hits the protected endpoint.

Reword this:

--
If the Client is a regular web app executing on a server, then the Authorization Code Flow is the flow you should use.
Using this the Client can retrieve an Access Token and, optionally, a Refresh Token.
It's considered the safest choice since the Access Token is passed directly to the web server hosting the Client,
without going through the user's web browser and risking exposure.

Authorization Code Flow
Because regular web apps are server-side apps where the source code is not publicly exposed, they can use the Authorization Code Flow (defined in OAuth 2.0 RFC 6749, section 4.1), which exchanges an Authorization Code for a token. Your app must be server-side because during this exchange, you must also pass along your application's Client Secret, which must always be kept secure, and you will have to store it in your client.

--

# Auth0 web & API auth 
 
This repo is showing how to write a web app that gets authenticated using Auth0 & uses an API token to hit a protected endpoint through a python client.
It also implements the use of `Authorization code` to request API access tokens: [Official documentation](https://auth0.com/docs/authorization/flows/call-your-api-using-the-authorization-code-flow#request-tokens)

## Run
Get the AUTH0_DOMAIN, AUTH0_CLIENT_SECRET, AUTH0_CLIENT_ID, AUTH0_API_CLIENT_ID, AUTH0_API_CLIENT_SECRET from Auth0. Replace the values in the `.env.example` and rename the file to `.env`. Execute:
```shell
sh start.sh
```
In a real scenario:
- A web app (could be mobile app, cli, another type of app) authenticates against Auth0.
- If the login was successful, using API_SECRET_ID & API_SECRET_PASSWORD it hits Auth0 again to request an API token with those credentials
- If API_SECRET_ID & API_SECRET_PASSWORD are valid then, Auth0 generates and sends an API token to the client.
- The client includes this token to interact with the API (the API here is an API developed to be the backend of the app). Auth0 also has an APi but the code in this repo is not interacting with that API yet.

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

## Run

Execute in another terminal the following command, to get into the container:
```shell
docker exec -it python-auth0 bash 
```
Once inside the container, execute:

```shell
python client/api_client.py
```

## Notes:

The env variable `FLASK_APP=app.py` indicates the file that contains the flask application. If this env variable is set the command to run the application is `flask run --reload` (for development). If this variable is not passed through the way to run the application is with `python app.py -h 0.0.0.0`.
The outcome should be: `Oh happy day!`

## TODO

Update the code according to this: https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https