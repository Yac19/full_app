#!/bin/bash
cd /var/run/fail2ban
rm fail2ban.sock fail2ban.pid
service fail2ban start

# Lancer le serveur Nginx en premier plan
nginx -g "daemon off;"