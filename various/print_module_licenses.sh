: << 'COMMENT'
written in bash
author : K.A.Draziotis
Licence : GPL
COMMENT
#!/bin/sh
number_of_modules=$(lsmod|wc -l)
a=$(lsmod |awk '{print $1}'|awk 'NR>1')

for mods in $a
do         
    b=$(/sbin/modinfo $mods|grep license|awk '{print $2$3$4$5}'|awk 'NR<=1')
    c=$(/sbin/modinfo $mods|grep description|awk '{print $2$3$4$5}'|awk 'NR<=1')
    printf -- '%-35s %-35s %-5s %-s\n\n' "$mods" "$b" "$c">&2   
done | column -t
printf -- 'you have: %d kernel modules. \n' "$number_of_modules" >&2
