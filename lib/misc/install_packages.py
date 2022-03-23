import sys
import subprocess
filename = 'packages'

with open(filename) as f:
    packagepackage = f.read().splitlines()

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'pipwin'])

for line in packagepackage:
    try:
        # implement pip as a subprocess:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install',
        line])
    except:
        # implement pip as a subprocess:
        subprocess.check_call([sys.executable, '-m', 'pipwin', 'install',
                               line])


# process output with an API in the subprocess module:
reqs = subprocess.check_output([sys.executable, '-m', 'pip',
'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

print(installed_packages)