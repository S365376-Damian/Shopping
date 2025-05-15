#!/bin/bash
mongodump --host localhost --port 27017  --username vohungvi --password viscomsolution --out /var/tmdt/backup_db --db tmdt
cd /var/tmdt/backup_db
tar -czvf /var/tmdt/download/tmdt_database.tar.gz tmdt