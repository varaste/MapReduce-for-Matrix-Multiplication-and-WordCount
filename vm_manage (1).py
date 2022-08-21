import requests
import time
import paramiko
from subprocess import PIPE, run

vms = {'vm1': 'http://192.168.1.102/', 'vm2': 'http://192.168.1.103/', 'vm3': 'http://192.168.1.104/'}


# load_balancer = '192.168.1.62'
def get_cpu_usage(vm_list):
    vm_cpu_usage = {}
    for vm_name, vm_ip in vm_list.items():
        try:
            r = requests.get(vm_ip + 'c.txt', timeout=5)
            vm_cpu_usage[vm_name] = r.content.decode("utf-8")
        except Exception as e:
            vm_cpu_usage[vm_name] = -1.0
    return vm_cpu_usage


host = '192.168.1.105'
port = 22
username = "reza"
password = "19422010"
command = "ls"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)
stdin, stdout, stderr = ssh.exec_command(command)
lines = stdout.readlines()
print(lines)
while True:
    cpu_usage_hist = get_cpu_usage(vms)
    # vm_cpu = get_cpu_usage(v)
    print(cpu_usage_hist)
    # print(f"{k}'s CPU usage is {vm_cpu}")
    # vm2_on_off_check = 'vboxmanage showvminfo "your_vm_name" | grep -c "running (since"'
    if float(cpu_usage_hist.get('vm1', 0)) > 60.0:
        if float(cpu_usage_hist.get('vm2', 0)) == -1.0:
            print('higher than threshold' + 'vm1')

            command = ["VBoxManage", "startvm", 'vm2F']
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            stdin, stdout, stderr = ssh.exec_command('python3 /home/reza/prox/p.py vm2 on')
            lines = stdout.readlines()
            # print(lines)
            if not (len(result.stderr) > 5):
                print('starting vm2')

            else:
                print('vm2 is already running')
    if (float(cpu_usage_hist.get('vm1', 0)) + float(cpu_usage_hist.get('vm2', 0))) > 120.0:
        if float(cpu_usage_hist.get('vm3', 0)) == -1.0:
            print('higher than threshold' + 'vm1 and vm2')

            command = ["VBoxManage", "startvm", 'vm3F']
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            stdin, stdout, stderr = ssh.exec_command('python3 /home/reza/prox/p.py vm3 on')
            lines = stdout.readlines()
            print(lines)
            if not (len(result.stderr) > 5):
                print('starting vm3')

            else:
                print('vm3 is already running')

    if (float(cpu_usage_hist.get('vm1', 0)) + float(cpu_usage_hist.get('vm2', 0)) + float(
            cpu_usage_hist.get('vm3', 0))) < 70.0:
        if float(cpu_usage_hist.get('vm2', 0)) != -1.0 and float(cpu_usage_hist.get('vm3', 0)) != -1.0:
            print('shutting down vm3 if not off')
            command = ["VBoxManage", "controlvm", "vm3F", "poweroff"]
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            stdin, stdout, stderr = ssh.exec_command('python3 /home/reza/prox/p.py vm3 off')
            lines = stdout.readlines()
            print(lines)
            if not (len(result.stderr) > 5):
                print('lower than threshold' + 'vm1 and vm2 and vm3')

            else:
                pass
    if (float(cpu_usage_hist.get('vm1', 0)) + float(cpu_usage_hist.get('vm2', 0))) < 20.0:
        if float(cpu_usage_hist.get('vm2', 0)) != -1.0 and float(cpu_usage_hist.get('vm3', 0)) == -1.0:
            print('shutting down vm2 if not off')
            command = ["VBoxManage", "controlvm", "vm2F", "poweroff"]
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            stdin, stdout, stderr = ssh.exec_command('python3 /home/reza/prox/p.py vm2 off')
            lines = stdout.readlines()
            print(lines)
            if not (len(result.stderr) > 5):
                print('lower than threshold' + 'vm1 and vm2')



        else:
            pass
    print()
    time.sleep(60)
