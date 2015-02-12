
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

3. `vagrant up`
4. `ssh-add`
5. `ansible-playbook -i hosts -e "env=vagrant" standards/setup.yml`
6. `ansible-playbook -i hosts -e "env=vagrant" setup.yml -vvvv`
7. `ansible-playbook -i hosts -e "env=vagrant" deploy.yml -e git_tag=devel -vvvv`
8. Run

        . /srv/frontend/ganymede-friends/env/current/bin/activate
        export PYTHONPATH=/srv/frontend/ganymede-friends/releases/current:/srv/frontend/ganymede-friends/releases/current/ganymede:/srv/frontend/ganymede-friends/env/current/lib/python2.7/site-packages
        python /srv/frontend/ganymede-friends/releases/current/ganymede/server_motor.py

# Variables

See roles/settings/defaults/main.yml


