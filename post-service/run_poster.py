import posts
import time
import subprocess
with open('test','w') as f:
    f.write('started')

def status():
    return subprocess.check_output(
            ['gcloud', 'compute', 'instances', 'list']
            ).decode('utf8').split('\n')[-2]

def start():
    subprocess.call(
            ['gcloud', 'compute', 'instances', 'start', 'mc-server']
            ).decode('utf8')
    return 'True'

def stop():
    subprocess.call(
            ['gcloud', 'compute', 'instances', 'stop', 'mc-server']
            ).decode('utf8')
    return 'False'

def system(arg):
    return subprocess.check_output(
            arg
        ).decode('utf8')
    

cmds = {
        'status': status,
        'start': start,
        'shutdown': stop,
        'help': 'status, start, shutdown, help',
        'system*': system,
    }
time.sleep(4)
server = posts.Server(cmds)
print("Server starts")
server.loop()
