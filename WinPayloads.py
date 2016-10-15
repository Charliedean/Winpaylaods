#!/usr/bin/python
from lib.main import *
from lib.payloadextras import *
from lib.startmetasploit import *
from lib.menu import *
from lib.sockets import *

try:
    from lib.psexecspray import *
except:
    print t.bold_red + "[!] Rerun the setup.sh" + t.normal

if not re.search('winpayloads', os.getcwd().lower()):
    print t.bold_red + "[!!] Please Run From Winpayloads Dir" + t.normal
    sys.exit(1)

try:
    os.mkdir('/etc/winpayloads')
except OSError:
    pass

try:
    print t.bold_green + "Checking if up-to-date || ctr + c to cancel" + t.normal
    checkupdate = subprocess.Popen(['git','pull','--dry-run'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    LOADING = Spinner('Checking...')
    while checkupdate.poll() == None:
        LOADING.Update()
        time.sleep(0.2)
    print '\r',
    sys.stdout.flush()
    if checkupdate.stderr.read():
        updateornah = raw_input(t.bold_red + "Do you want to update WinPayloads? Y/[N]: " + t.normal)
        if updateornah.upper() == "Y":
            p = subprocess.Popen(['git','pull'])
            p.wait()
            print t.bold_yellow + "Re-run setup.sh and reload Winpayloads..." + t.normal
            sys.exit()
except KeyboardInterrupt:
    pass

worker = Thread(target=startClientListener)
worker.setDaemon(True)
worker.start()

try:
    getAndRunMainMenu()
except KeyboardInterrupt:
    print t.bold_green + '\n[*] Cleaning Up\n' + t.normal
    subprocess.call(['rm *.rc'], shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.call(['rm *.ps1'], shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.call(['rm logdict*'], shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sys.exit()
