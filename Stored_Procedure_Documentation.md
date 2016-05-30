## Stored Procedure Documentation

---
### Stored Procedures
---
#### Create Tenant Login
```sh
Stored Procedure : [crosstagAdminSchema].[CreateTenantLogin]
Method : CREATE
Params : username, string(50). password, string(200). active_fortnox, string(10). gym_name, string(50). address, string(50). phone, string(20). zip_code, string(20). city, string(50). email, string(50). loginPass, string(50).
Return : 1 if success. 0 if fail.
Raises : 
Description : Creates a Database login, Database User, Database Schema, Adds Database User to AppRole, Runs Register Tenant, Runs Create User Table, Runs Create Debt Table, Runs Create Statistic Tagevents, Runs Create Detailed Tagevents Table
```


#### Register Tenant
```sh
Stored Procedure : [crosstagAdminSchema].[RegisterTenant] 
Method : CREATE
Params : username, string(50). password, string(200). active_fortnox, string(10). gym_name, string(50). address, string(50). phone, string(20). zip_code, string(20). city, string(50). email, string(50). 
Return : 
Raises : FailError
Description : Register a new Tenant and the Tenanants Gym Info
```


#### Create User Table
```sh
Stored Procedure : [crosstagAdminSchema].[CreateUserTable]
Method : CREATE
Params : schema, string(25)
Return : 
Raises : FailError
Description : Create a table where the Tenant saves all users(Gym Members)
```

#### Create Debt Table
```sh
Stored Procedure : [crosstagAdminSchema].[CreateDebtTable]
Method : CREATE
Params : schema, string(25)
Return : 
Raises : FailError
Description : Create a table where the Tenant saves all Debts
```

#### Create Statistic Tagevents Table
```sh
Stored Procedure : [crosstagAdminSchema].[CreateStatisticTagevents]
Method : CREATE
Params : schema, string(25)
Return : 
Raises : FailError
Description : Create a table where the Tenant saves all Tagevents for statistic
```

#### Create Detailed Tagevents Table
```sh
Stored Procedure : [crosstagAdminSchema].[CreateDetailedtageventsTable]
Method : CREATE
Params : schema, string(25)
Return : 
Raises : FailError
Description : Create a table where the Tenant saves all Tagevents ub detail
```

#### Update Tenants Account Info
```sh
Stored Procedure : [crosstagAdminSchema].[UpdateTenant] 
Method : UPDATE
Params : id, integer. password, string(200). active_fortnox, string(10). image, string(MAX). background_color, string(10). new_password, string(200). 
Return : 
Raises : FailError
Description : Update a Tenants account info
```

#### Update Tenants Gym Info
```sh
Stored Procedure : [crosstagAdminSchema].[UpdateGymInfo]
Method : UPDATE
Params : id, integer. password, string(200). gym_name, string(50). address, string(50). phone, string(20). zip_code, string(20). city, string(50). email, string(50). 
Return : 
Raises : FailError
Description : Update a Tenants contact and gym info
```

#### Update Tenants Fortnox Info
```sh
Stored Procedure : [crosstagAdminSchema].[UpdateFortnox]
Method : UPDATE
Params : id, integer. password, string(200). client_secret, string(200). access_id, string(200).
Return : 
Raises : FailError
Description : Update a Tenants Fortnox info
```

#### Login Tenant
```sh
Stored Procedure : [crosstagAdminSchema].[LoginTenant]
Method : READ
Params : username, string(50)
Return : Hashed password
Raises : 
Description : If username exists, return hashed password for comparision in the code.
```

#### Get Tenant With Api Key
```sh
Stored Procedure : [crosstagAdminSchema].[GetTenantWithApiKey] 
Method : READ
Params : apikey, string(MAX)
Return : Username
Raises : 
Description : If apikey exists, return username matching the api key
```

#### Get Tenant(s)
```sh
Stored Procedure : [crosstagAdminSchema].[GetTenants]
Method : READ
Params : username, string(50)
Return : Tenant
Raises : 
Description : If username is empty, return all tenants. If username contains a name, return matching tenant info. 
```


