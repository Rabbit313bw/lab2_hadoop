#!/bin/bash

echo "Run spark app..."

cd "$(dirname "$0")"


chmod 1777 logs

docker exec -it spark spark-submit /home/jovyan/app/app.py
docker exec -it spark spark-submit /home/jovyan/app/app_opt.py


echo "Done"