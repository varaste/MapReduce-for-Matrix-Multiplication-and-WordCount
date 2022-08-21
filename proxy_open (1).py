import sys
from subprocess import PIPE, run

vm_no = sys.argv[1]
toggle = sys.argv[2]
print(vm_no)
print(toggle)

with open("/etc/haproxy/haproxy.cfg", 'r') as f:
    get_all = f.readlines()

with open("/etc/haproxy/haproxy.cfg", 'w') as f:
    for i, line in enumerate(get_all, 1):
        if i == 41:
            if vm_no == 'vm2':
                if toggle == 'on':
                    if line.startswith('#'):
                        line = line[1:]
                        f.writelines(line)
                    else:
                        f.writelines(line)
                elif toggle == 'off':
                    if not line.startswith('#'):
                        line = '#' + line
                        f.writelines(line)
                    else:
                        f.writelines(line)
            else:
                f.writelines(line)
        elif i == 42:
            if vm_no == 'vm3':
                if toggle == 'on':
                    if line.startswith('#'):
                        line = line[1:]
                        f.writelines(line)
                    else:
                        f.writelines(line)
                elif toggle == 'off':
                    if not line.startswith('#'):
                        line = '#' + line
                        f.writelines(line)
                    else:
                        f.writelines(line)
            else:
                f.writelines(line)
        else:
            f.writelines(line)

command = ['sudo', 'iptables', '-I', 'INPUT', '-p', 'tcp', '--dport', '80', '--syn', '-j', 'DROP']
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

command = ['sleep', '1']
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

command = ['sudo', 'systemctl', 'restart', 'haproxy.service']
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

command = ['sudo', 'iptables', '-D', 'INPUT', '-p', 'tcp', '--dport', '80', '--syn', '-j', 'DROP']
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
