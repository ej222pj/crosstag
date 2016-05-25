## API Documentation

---
### Methods

---
#### Create tagevent
```sh
Request : /crosstag/v1.0/tagevent/<tag_id>/<api_key>/<timestamp>
Method : GET
Params : tag_id, string. api_key, string. timestamp, string.
Return : Redirect or renders template
Raises : KeyError
Description : Gets a tagevent from crosstag_reader with tag_id, api_key and timestamp of the tagevent. Checks if the api-key is valid and then creates the tag and saves it in the database. If the api-key is wrong a KeyError is raised.
```

#### Remove User
```sh
Request : /crosstag/v1.0/remove_user/<user_id>
Method : POST
Params : user_id, integer
Return : Redirect
Description : Deletes a user from the database.
```

#### Link user to last tag
```sh
Request : /crosstag/v1.0/link_user_to_last_tag/<user_id>
Method : GET/POST
Params : user_id, integer
Return : Redirect
Description : Links the user to the last tag. Grabs the last tag stored in the database and binds it to the specified member. Grabs only a tag that doesnt belong to another member.
```

#### Sync from Fortnox
```sh
Request : /crosstag/v1.0/fortnox/
Method : GET
Params :
Return : Redirect
Description : Syncs the database with users from fortnox database. Add or updates the users.
```


