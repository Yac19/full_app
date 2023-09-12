#!/bin/bash
cd /var/run/fail2ban
rm fail2ban.sock fail2ban.pid
service fail2ban start

# Lancer en arrière plan
fail2ban-client start

# Lancer le serveur Nginx en premier plan
nginx -g "daemon off;"
