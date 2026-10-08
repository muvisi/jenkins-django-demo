#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=========================================="
echo " Jenkins Django Demo - VPS Reset"
echo "=========================================="
echo "Target VPS: 66.23.236.42"
echo

if [[ ! -f ansible/reset.yml ]]; then
    echo "ERROR: ansible/reset.yml not found."
    exit 1
fi

echo "Checking Ansible syntax..."
ansible-playbook \
    -i ansible/inventory.ini \
    ansible/reset.yml \
    --syntax-check

echo
echo "WARNING: This removes the Django demo deployment"
echo "and any local application data on the VPS."
read -r -p "Type RESET to continue: " CONFIRM

if [[ "$CONFIRM" != "RESET" ]]; then
    echo "Cancelled."
    exit 0
fi

echo
echo "Enter the VPS SSH and sudo passwords when prompted."

ansible-playbook \
    -i ansible/inventory.ini \
    ansible/reset.yml \
    -u deploy \
    --ask-pass \
    --ask-become-pass

echo
echo "SUCCESS: Reset playbook completed."
