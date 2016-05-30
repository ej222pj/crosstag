# Stored Procedure Documentation
[Application Specific Stored Procedures](https://github.com/ej222pj/crosstag/blob/master/Stored_Procedure_Documentation.md#aplication-specific-stored-procedures)
[Tenant Specific Stored Procedures](https://github.com/ej222pj/crosstag/blob/master/Stored_Procedure_Documentation.md#tenant-specific-stored-procedures-1)
---
## Aplication Specific Stored Procedures
#### Schema: [crosstagAdminSchema]
---

### Create Tenant Login
```sh
Stored Procedure [CreateTenantLogin]
Method : CREATE
Params : username, string(50). password, string(200). active_fortnox, string(10). gym_name, string(50). address, string(50). phone, string(20). zip_code, string(20). city, string(50). email, string(50). loginPass, string(50).
Return : 1 if success. 0 if fail.
Raises : 
Description : Creates a Database login, Database User, Database Schema, Adds Database User to AppRole, Runs [RegisterTenant], Runs [CreateUserTable], Runs [CreateDebtTable], Runs [CreateStatisticTagevents], Runs [CreateDetailedTageventsTable].
```

### Register Tenant
```sh
Stored Procedure : [RegisterTenant] 
Method : CREATE
Params : username, string(50). password, string(200). active_fortnox, string(10). gym_name, string(50). address, string(50). phone, string(20). zip_code, string(20). city, string(50). email, string(50). 
Return : 
Raises : FailError
Description : (Is only runned by [CreateTenantLogin]) Register a new Tenant and the Tenanants Gym Info
```


### Create User Table
```sh
Stored Procedure : [CreateUserTable]
Method : CREATE
Params : schema, string(25)
Return : 
Raises : FailError
Description : (Is only runned by [CreateTenantLogin]) Create a table where the Tenant saves all users(Gym Members)
```

### Create Debt Table
```sh
Stored Procedure : [CreateDebtTable]
Method : CREATE
Params : schema, string(25)
Return : 
Raises : FailError
Description : (Is only runned by [CreateTenantLogin]) Create a table where the Tenant saves all Debts
```

### Create Statistic Tagevents Table
```sh
Stored Procedure : [CreateStatisticTagevents]
Method : CREATE
Params : schema, string(25)
Return : 
Raises : FailError
Description : (Is only runned by [CreateTenantLogin]) Create a table where the Tenant saves all Tagevents for statistic
```

### Create Detailed Tagevents Table
```sh
Stored Procedure : [CreateDetailedtageventsTable]
Method : CREATE
Params : schema, string(25)
Return : 
Raises : FailError
Description : (Is only runned by [CreateTenantLogin]) Create a table where the Tenant saves all Tagevents ub detail
```

### Update Tenants Account Info
```sh
Stored Procedure : [UpdateTenant] 
Method : UPDATE
Params : id, integer. password, string(200). active_fortnox, string(10). image, string(MAX). background_color, string(10). new_password, string(200). 
Return : 
Raises : FailError
Description : Update a Tenants account info
```

### Update Tenants Gym Info
```sh
Stored Procedure : [UpdateGymInfo]
Method : UPDATE
Params : id, integer. password, string(200). gym_name, string(50). address, string(50). phone, string(20). zip_code, string(20). city, string(50). email, string(50). 
Return : 
Raises : FailError
Description : Update a Tenants contact and gym info
```

### Update Tenants Fortnox Info
```sh
Stored Procedure : [UpdateFortnox]
Method : UPDATE
Params : id, integer. password, string(200). client_secret, string(200). access_id, string(200).
Return : 
Raises : FailError
Description : Update a Tenants Fortnox info
```

### Login Tenant
```sh
Stored Procedure : [LoginTenant]
Method : READ
Params : username, string(50)
Return : Hashed password
Raises : 
Description : If username exists, return hashed password for comparision in the code.
```

### Get Tenant With Api Key
```sh
Stored Procedure : [GetTenantWithApiKey] 
Method : READ
Params : apikey, string(MAX)
Return : Username
Raises : 
Description : If apikey exists, return username matching the api key
```

### Get Tenant(s)
```sh
Stored Procedure : [GetTenants]
Method : READ
Params : username, string(50)
Return : Tenant
Raises : 
Description : If username is empty, return all tenants. If username contains a name, return matching tenant info. 
```

## Tenant Specific Stored Procedures
#### Schema: [dbo]
---

### Add User
```sh
Stored Procedure : [AddUser]
Method : CREATE
Params : fortnox_id, string(10). firstname, string(25). lastname, string(30). email, string(120). phone, string(20). address, string(50). address2, string(50). city, string(120). zip_code, string(10). tag_id, string(20). gender, string(10). ssn, string(13). expiry_date, string(30). create_date, string(30). status, string(50). tagcounter, integer. last_tag_timestamp, string(30).
Return : 
Raises : FailError 
Description : Creates a new User
```

### Add Debt
```sh
Stored Procedure : [AddDebt]
Method : CREATE
Params : amount, integer. product, string(60). create_date, date(7). uid, integer.
Return : 
Raises : FailError 
Description : Creates a new Debt
```

### Add Detailed Tagevent
```sh
Stored Procedure : [AddDetailedTagevents]
Method : CREATE
Params : tag_id, string(20). timestamp, date(7). hourNow, integer. uid, integer.
Return : 
Raises : FailError 
Description : Creates a new Detailed Tagevent and runs [AddStatisticTagevents]
```

### Add Statistic Tagevent
```sh
Stored Procedure : [AddStatisticTagevents]
Method : CREATE
Params : timestamp, date(7). amount, integer. clockstamp, integer.
Return : 
Raises : FailError 
Description : (This stored proc is only used by [AddDetailedTagevents]) Creates a new row for statistic tagevents. Updates if a new tagevent occurs on the same hour. If it's a new hour, create a new row.
```

### Update User
```sh
Stored Procedure : [UpdateUser]
Method : UPDATE
Params : id, integer. firstname, string(25). lastname, string(30). email, string(120). phone, string(20). address, string(50). address2, string(50). city, string(120). zip_code, string(10). tag_id, string(20). gender, string(10). ssn, string(13). expiry_date, date(7). status, string(50).
Return : 
Raises : FailError
Description : Update Info on a User
```

### Update Debt
```sh
Stored Procedure : [UpdateDebt]
Method : UPDATE
Params : id, integer. amount, integer. product, string(60). 
Return : 
Raises : FailError
Description : Update a Debt
```

### Update Statistic Tagevent
```sh
Stored Procedure : [UpdateStatisticTagevents]
Method : UPDATE
Params : id, integer.
Return : 
Raises : FailError
Description : Update the current row for statistic tagevent if a new tagevent occured.
```

### Search User
```sh
Stored Procedure : [SearchUsers]
Method : READ
Params : firstname, string(25). lastname, string(30). email, string(120). city, string(120).
Return : All matching Users
Raises : 
Description : Search if for one or all of the inputs and returns all matching users.
```

### Search User On Tag
```sh
Stored Procedure : [SearchUserOnTag]
Method : READ
Params : tag_id, string(MAX).
Return : User
Raises : 
Description : If tag_id is connected to a user, return that user
```

### Get User ID
```sh
Stored Procedure : [GetUserId]
Method : READ
Params : fortnox_id, string(10).
Return : User.id
Raises : 
Description : If fortnox_id is connected to a user, return that users id
```

### Get User(s)
```sh
Stored Procedure : [GetUser]
Method : READ
Params : id, integer.
Return : User
Raises : 
Description : If id is 0, get all users. If id is > 0, get the user with that id.
```

### Get Statistic Tagevents
```sh
Stored Procedure : [GetStatisticTagevents]
Method : READ
Params : id, integer.
Return : Statistic Tagevent
Raises : 
Description : If id is 0, get all statistic tagevents. If id is > 0, get the tagevent with that id.
```

### Get Inactive Users
```sh
Stored Procedure : [GetInactiveUsers] 
Method : READ
Params :
Return : User
Raises : 
Description : Get all users with active membership that has not tagged for 2 weeks
```

### Get Detailed Tagevent(s)
```sh
Stored Procedure : [GetDetailedTagevents] 
Method : READ
Params : uid, integer. numberOfTagevents, integer.
Return : Detailed tagevents
Raises : 
Description : If uid = 0 and numberOfTagevents = 1, get the last tagevent. If uid = 0 and numberOfTagevents > 1 get as many as numberOfTagevents says. If uid > 0 get tagevents for a specific user.
```

### Get Debt(s)
```sh
Stored Procedure : [GetDebt]
Method : READ
Params : uid, integer.
Return : Debt
Raises : 
Description : If uid = 0, get all Debts. If uid > 0, get Debts for specific user.
```

### Does User Exsts
```sh
Stored Procedure : [DoesUserExists]
Method : READ
Params : fortnox_id, string(10).
Return : 1 if User exist or 0 if user don't exist
Raises : 
Description : Check if a user already exist from Fortnox. 
```

### Delete User
```sh
Stored Procedure : [DeleteUser]
Method : DELETE
Params : id, integer.
Return : 
Raises : FailError 
Description : Delete a user based on the ID
```

### Delete Debt
```sh
Stored Procedure : [DeleteDebt]
Method : DELETE
Params : id, integer.
Return : 
Raises : FailError 
Description : Delete a Debt based on the ID
```
