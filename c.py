import json
import subprocess

while True:
    cpu_stat = subprocess.run(['mpstat', '120', '1', '-o', 'JSON'], stdout=subprocess.PIPE)
    cpu_usage = 100 - float(json.loads(cpu_stat.stdout)['sysstat']['hosts'][0]['statistics'][0]['cpu-load'][0]['idle'])
    f = open('/var/www/html/c.txt', 'w')
    f.write(str(cpu_usage))
    f.close()
    print('finito')
