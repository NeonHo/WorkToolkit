
field_name = input("Enter the field name: ")
field_name_simple = input("Enter the field name simple (Yungang is yg): ")
station_name = input("Enter the station name: ")
ip_address = input("Enter the IP address: ")
vlan_guanli = input("Enter the VLAN for guanli: ")
vlan_yewu = input("Enter the VLAN for yewu: ")
trunk_ip = input("Enter the trunk IP: ")

name_str = f"""
sysname {field_name}#{station_name}_{ip_address}
clock timezone beijing add 08:00:00
"""

unable_global_config = f"""
undo lldp global enable
stp global enable
undo ip http enable
undo ip https enable
undo telnet server enable 
undo ntp enable 
undo password-control enable
"""

ssh_port_str = f"""
ssh server port 22022
"""

interface_shutdown_str = f"""
interface Vlan-interface1
shutdown
quit

interface M-GigabitEthernet0/0/0
shutdown
quit

interface range Ten-GigabitEthernet 1/0/49 to Ten-GigabitEthernet 1/0/54
shutdown
quit
"""

vlan_str = f"""
vlan {vlan_guanli}
description guanli
quit
vlan {vlan_yewu}
description yewu
quit
"""

acl_str = f"""
acl number 2000
rule 10 permit source 22.39.6.16 0.0.0.15
quit

acl number 2010
rule 3 permit source 21.38.0.12 0
rule 5 permit source 21.38.0.14 0
rule 6 permit source 21.38.0.15 0
rule 10 permit source 21.38.0.7 0
rule 11 permit source 21.38.0.8 0
rule 15 permit source 25.39.75.170 0
rule 16 permit source 25.39.75.191 0
rule 17 permit source 25.39.75.193 0
quit

acl number 3000
rule 1 deny tcp destination-port eq 135
rule 2 deny tcp destination-port eq 137
rule 3 deny tcp destination-port eq 138
rule 4 deny tcp destination-port eq 139
rule 5 deny tcp destination-port eq 445
rule 7 deny tcp destination-port eq 1433
rule 9 deny tcp destination-port eq 1434
rule 13 deny tcp destination-port eq 1413
rule 15 deny tcp destination-port eq 3389
rule 17 deny udp destination-port eq 135
rule 18 deny udp destination-port eq netbios-ns
rule 19 deny udp destination-port eq netbios-dgm
rule 20 deny udp destination-port eq netbios-ssn
rule 21 deny udp destination-port eq 445
rule 30 deny udp destination-port eq 1413
rule 33 deny udp destination-port eq 1433
rule 35 deny udp destination-port eq 1434
quit
"""

ip_str = f"""
interface Vlan-interface {vlan_guanli}
ip address {ip_address} 255.255.255.128
quit
"""

enthernet_str = f"""
interface range  GigabitEthernet1/0/1 to GigabitEthernet1/0/47
port access vlan {vlan_yewu}
ip verify source ip-address mac-address
undo poe enable
quit

interface GigabitEthernet1/0/48
port link-type trunk
undo port trunk permit vlan 1
port trunk permit vlan {vlan_guanli} {vlan_yewu}
undo poe enable
undo stp enable
packet-filter 3000 inbound
quit
"""

loop_str = f"""
loopback-detection global enable vlan {vlan_yewu}
ip route-static 0.0.0.0 0 {trunk_ip}
ntp-service unicast-server 10.100.48.7
info-center loghost source Vlan-interface {vlan_guanli}
info-center loghost 21.38.0.11
"""

manage_str = f"""
local-user xtsjzx class manage
password simple DT{field_name_simple}@xt.2026
service-type ssh
authorization-attribute user-role network-admin
quit
"""

snmp_str = f"""
snmp-agent
snmp-agent community read simple dtgd@xtgs acl 2010
snmp-agent sys-info version v2c v3
"""

ssh_config_str = f"""
ssh server enable
ssh user xtsjzx service-type stelnet authentication-type password
ssh server acl 2000
"""

line_str = f"""
line vty 0 15
authentication-mode scheme
user-role network-admin
protocol inbound ssh
idle-timeout 5 0
quit

line con 0
authentication-mode password
user-role network-admin
set authentication password simple DTgd!@#$2026
idle-timeout 5 0
quit
"""

schedule_str = f"""
scheduler job beifen
command 1 save force
command 2 tftp 21.38.0.34  put config.cfg  {ip_address}_config.cfg
quit

scheduler schedule beifen
job beifen
time repeating at 00:00 month-date 1
quit
"""

test_str = f"""
interface GigabitEthernet 1/0/1
port access vlan {vlan_guanli}
undo ip verify source
quit

undo ssh server acl
"""

recover_str = f"""
interface GigabitEthernet 1/0/1
port access vlan {vlan_yewu}
ip verify source ip-address mac-address
quit

ssh server acl 2000
"""

# output to file
with open(f"{field_name}#{station_name}_{ip_address}.cfg", "w") as f:
    f.write(name_str)
    f.write('\n')
    f.write(unable_global_config)
    f.write('\n')
    f.write(ssh_port_str)
    f.write('\n')
    f.write(interface_shutdown_str)
    f.write('\n')
    f.write(vlan_str)
    f.write('\n')
    f.write(acl_str)
    f.write('\n')
    f.write(ip_str)
    f.write('\n')
    f.write(enthernet_str)
    f.write('\n')
    f.write(loop_str)
    f.write('\n')
    f.write(manage_str)
    f.write('\n')
    f.write(snmp_str)
    f.write('\n')
    f.write(ssh_config_str)
    f.write('\n')
    f.write(line_str)
    f.write('\n')
    f.write(schedule_str)
    f.write('\n')
    f.write(test_str)
    f.write('\n')
    f.write(recover_str)
    f.write('\n')