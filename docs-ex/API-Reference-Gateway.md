NWApp API Web-Service Reference (Gateway)
======

## Developers Notes

1. To help make the next few API endpoints easy to type, save your token to the console.

    ```bash
    NWAPP_BACK_API_TOKEN='YOUR_TOKEN'
    ```

2. You will notice ``http`` used in the sample calls through this document, this is the ``Python`` command line application called ``HTTPie``. Download the command line application by following [these instructions](https://httpie.org/).

3. If you are going to make any contributions, please make sure your edits follow the [API documentation standard](https://gist.github.com/iros/3426278) for this document; in addition, please read [Googles API Design Guide](https://cloud.google.com/apis/design/) for further consideration.


## Register (TODO: PENDING IMPLEMENTATION)
Submit registration details into our system to automatically create a *user* account. System return the *user* details and authentication *token*.

Created *user* accounts are automatically granted access to the system even though these accounts have not had their email verified. The system sends a verification email after creation and if the *user* does not verify in the allotted timespan, their account gets locked.

It's important to note that emails must be unique and passwords strong or else validation errors get returned.

* **URL**

  ``/api/v1/register``


* **Method**

  ``POST``


* **URL Params**

  None


* **Data Params**

  * email
  * password
  * first_name
  * last_name


* **Success Response**

  * **Code:** 200
  * **Content:**

    ```json

    ```


* **Error Response**

  * **Code:** 400
  * **Content:**

    ```json
    {
        "error": "Email is not unique.",
        "status": "Invalid request."
    }
    ```


* **Sample Call**

  ```bash
  $ http post localhost:80/api/v1/public/register \
    email=bart@mikasoftware.com \
    password=YOUR_PASSWORD \
    first_name=Bart \
    last_name=Mika
  ```


## Login
Returns the *user profile* and authentication *token* upon successful login in.

* **URL**

  ``/api/v1/login``


* **Method**

  ``POST``


* **URL Params**

  None


* **Data Params**

  * email
  * password


* **Success Response**

  * **Code:** 200
  * **Content:**

    ```json
    {
        "access_token": {
            "expires": 1573875899,
            "scope": "read,write,introspection",
            "token": "pwtYmgPCEwNXFUhPVjVNKcEBxYgvUz"
        },
        "email": "bart@mikasoftware.com",
        "first_name": "Bart",
        "group_membership_id": 1,
        "last_name": "Mika",
        "middle_name": null,
        "refresh_token": {
            "revoked": null,
            "token": "xWGpIbdDJRcLiy4R2wEfUOuDD252cB"
        },
        "schema_name": "public"
    }
    ```


* **Error Response**

  * **Code:** 400
  * **Content:**

    ```json
    {
        "error": "Email or password is incorrect.",
        "status": "Invalid request."
    }
    ```


* **Sample Call**

  ```bash
  $ http post localhost:80/api/v1/login \
    email=bart@mikasoftware.com \
    password=YOUR_PASSWORD
  ```

* **Notes**

  * If the server returned the access token value of ``pwtYmgPCEwNXFUhPVjVNKcEBxYgvUz`` then please make sure you write in your console ``NWAPP_BACK_API_TOKEN='pwtYmgPCEwNXFUhPVjVNKcEBxYgvUz'``.


## Logout
Performs logout operation for authenticated user thus invalidating the user's ``token``.

* **URL**

  ``/api/v1/logout``


* **Method**

  ``POST``


* **URL Params**

  None


* **Data Params**

  None


* **Success Response**

  * **Code:** 200
  * **Content:**

    ```json
    {
        "detail": "You are now logged off."
    }
    ```


* **Error Response**

  None


* **Sample Call**

  ```bash
  $ http post localhost:80/api/v1/logout token=$NWAPP_BACK_API_TOKEN Authorization:"Bearer $NWAPP_BACK_API_TOKEN"
  ```

* **Notes**

  * If the server returned the access token value of ``pwtYmgPCEwNXFUhPVjVNKcEBxYgvUz`` then please make sure you write in your console ``NWAPP_BACK_API_TOKEN='pwtYmgPCEwNXFUhPVjVNKcEBxYgvUz'``.


## Get Profile
The API endpoint used to get the *user profile details*. Only the *profile* of the *authenticated user* is returned.

* **URL**

  ``/api/v1/profile``


* **Method**

  ``GET``


* **URL Params**

  None


* **Data Params**

  None


* **Success Response**

  * **Code:** 200
  * **Content:**

    ```json
    {
        "email": "bart@mikasoftware.com",
        "first_name": "Bart",
        "last_name": "Mika",
        "user_id": 1
    }
    ```


* **Error Response**

  * None


* **Sample Call**

  ```bash
  $ http get localhost:80/api/v1/profile Authorization:"Bearer $NWAPP_BACK_API_TOKEN"
  ```


## Refresh Access Token
Function will take a non-expired ``refresh token`` and generate  new ``access token`` and ``refresh token`` and return them along with the user profile.

* **URL**

  ``/api/v1/refresh-token``


* **Method**

  ``POST``


* **URL Params**

  None


* **Data Params**

  None


* **Success Response**

  * **Code:** 200
  * **Content:**

    ```json
    {
    "access_token": {
        "expires": 1573877448,
        "scope": "read,write,introspection",
        "token": "q4rURV2BvY2xJpRcAhd8gMvRd5poFf"
    },
    "refresh_token": {
        "revoked": null,
        "token": "JXOkp0JDx60stiU2cjPGXdfX3LfaIQ"
    }
}

    ```


* **Error Response**

  None


* **Sample Call**

  ```bash
  $ http post localhost:80/api/v1/refresh-token refresh_token="xWGpIbdDJRcLiy4R2wEfUOuDD252cB" Authorization:"Bearer pwtYmgPCEwNXFUhPVjVNKcEBxYgvUz"
  ```

* **Notes**

  * Please update your ``NWAPP_BACK_API_TOKEN`` value in your terminal with the latest values returned by the API endpoint.
