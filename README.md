# TMDT


## How to run

### Import default database

Create database by cmd
```
mongo
```

```
use tmdt
```


```
db.createUser(
  {
    user: "vohungvi",
    pwd: "viscomsolution",
    roles: [ { role: "readWrite", db: "tmdt" } ]
  })

```

Import database: run file **restore_db.bat**

