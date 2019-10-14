#### Report
Example for checking migr2:
Run <code>python deploy.py check-migration  migr2</code>

```
tenant1:OK
tenant2:OK
tenant3:OK
tenant4:OK
tenant5:OK
tenant6:OK
tenant7:OK
tenant8:missing
tenant9:OK
tenant10:OK
tenant11:OK
tenant12:OK
tenant13:OK
tenant14:OK
tenant15:OK
tenant16:OK
tenant17:OK
tenant18:OK
tenant19:OK
tenant20:missing
```
For migr2, tenant8 and tenant20 don't have migrations because we didn't insert these migrations in the database.


Count the migrations for all the tenants:
Run <code>python3 deploy.py count-migrations</code>:
```
tenant1:24
tenant2:24
tenant3:24
tenant4:24
tenant5:24
tenant6:21
tenant7:21
tenant8:20
tenant9:21
tenant10:21
tenant11:20
tenant12:20
tenant13:20
tenant14:19
tenant15:20
tenant16:20
tenant17:20
tenant18:20
tenant19:20
tenant20:19
```

