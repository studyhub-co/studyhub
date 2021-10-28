#!/bin/bash

(cd /var/app/current; systemctl stop celery)
(cd /var/app/current; systemctl start celery)
(cd /var/app/current; systemctl enable celery.service)
