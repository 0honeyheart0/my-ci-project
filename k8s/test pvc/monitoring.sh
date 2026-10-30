#!/bin/bash

set -euo pipefail

echo "--disk--"
df / | awk 'NR==2 {print $5}' | tr -d '%'

echo "--OZU--"
free | awk ' /Mem:/ {print $3/$2 * 100}'

echo "--CPU--"
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1



