Vagrant Deployment
==================

### Deploying 'develop' version in Vagrant

1. Put your ssh key in ~/.ssh/id_rsa.pub
2. Make sure you have `ForwardAgent=yes` in your Ansible config (e.g. ~/.ansible.cfg):

        [defaults]
        transport = ssh

        [ssh_connection]
        ssh_args = -o ForwardAgent=yes
        pipelining=True

3. `git clone https://github.com/arturro/friends.git friends`
4.  `cd friends/ansible`
3. `vagrant up`
4. `ssh-add`
5. `ansible-playbook -i hosts -e "env=vagrant" full.yml -e git_tag=devel -vvvv`
6. `vagrant reload`
7. check: http://192.168.33.21:8000/friends/add/1/2 etc.



### manual start:

        ssh gmapp@192.168.33.21
        . /srv/frontend/ganymede-friends/env/current/bin/activate
        export PYTHONPATH=/srv/frontend/ganymede-friends/releases/current:/srv/frontend/ganymede-friends/releases/current/ganymede:/srv/frontend/ganymede-friends/env/current/lib/python2.7/site-packages
        python /srv/frontend/ganymede-friends/releases/current/ganymede/server_motor.py

or:

        ssh gmapp@192.168.33.21
        restart ganymede-friends



# Variables

See roles/settings/defaults/main.yml


