import os
from .conf import CK2USERFOLDER, SUVOROVMODFOLDER, SERVICEUNITFILE, PERMISSIONS

unitfilecontent = """
[Unit]
Description=suvorov

[Service]
Type=simple
ExecStart=/usr/bin/python3 -m suvorov.service
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
"""

def setup():

	os.makedirs(SUVOROVMODFOLDER,exist_ok=True)
	os.chown(SUVOROVMODFOLDER,PERMISSIONS.st_uid,PERMISSIONS.st_gid)
	try:
		os.makedirs(os.path.dirname(SERVICEUNITFILE),exist_ok=True)
		with open(SERVICEUNITFILE,"w") as unitfile:
			unitfile.write(unitfilecontent)
		print("Service successfully installed.")
	except PermissionError:
		print("Please run as administrator.")
		
		
