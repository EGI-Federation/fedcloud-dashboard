#!/bin/sh

set -e

SSH_KEY="$1"
IP="$2"

# Prepare the ansible setup
cat > inventory.yaml << EOF
all:
  hosts:
    $IP:
      ansible_user: egi
      ansible_ssh_private_key_file: key
      ansible_ssh_common_args: -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null
EOF

echo "$SSH_KEY" > key
chmod 400 key

# and now config
ansible-galaxy install -r galaxy-requirements.yaml

ansible-playbook -i inventory.yaml playbook.yaml
