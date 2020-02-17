import os
from .conf import CK2USERFOLDER, SUVOROVMODFOLDER, SERVICEUNITFILE

unitfilecontent = """
[Unit]
Description=Suvorov

[Service]
Type=simple
ExecStart=/usr/bin/python3 -m suvorov.service
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
"""

def setup():

	os.makedirs(SUVOROVMODFOLDER,exist_ok=True)
	stat = os.stat(CK2USERFOLDER)
	os.chown(SUVOROVMODFOLDER,stat.st_uid,stat.st_gid)
	try:
		os.makedirs(os.path.dirname(SERVICEUNITFILE),exist_ok=True)
		with open(SERVICEUNITFILE,"w") as unitfile:
			unitfile.write(unitfilecontent)
	except PermissionError:
		print("Please run as administrator.")
		
		
