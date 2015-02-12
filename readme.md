# INSTALATION

## requirements
Python 2.7
MongoDB

### Vagrant/Ansible

install:

*   Vagrant
*   Ansible
*   VirtualBox



TEST
====

python -m tornado.testing ganymede.users.tests.test_service_mongo

TODO
====
upstart
check log MongoDB
loadbalancing (Nginx/HAProxy)
test for 1M users with connection
compare with MySQL
