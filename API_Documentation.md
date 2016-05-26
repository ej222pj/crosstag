## API Documentation

---
### Methods

---
#### Create tagevent
```sh
Request : /crosstag/v2.0/tagevent/<tag_id>/<api_key>/<timestamp>
Method : GET
Params : tag_id, string. api_key, string. timestamp, string.
Return : Redirect or renders template
Raises : KeyError
Description : Gets a tagevent from crosstag_reader with tag_id, api_key and timestamp of the tagevent. Checks if the api-key is valid and then creates the tag and saves it in the database. If the api-key is wrong a KeyError is raised.
```


