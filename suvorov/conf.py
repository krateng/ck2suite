import os

METAFILE = "suvorov.yml"
SUVOROVSRCFOLDER = "."
VANILLASRCFOLDER = "pdx"
CK2USERFOLDER = os.path.expanduser("~/.paradoxinteractive/Crusader Kings II")
VANILLAMODFOLDER = os.path.join(CK2USERFOLDER,"mod")
SUVOROVMODFOLDER = os.path.join(CK2USERFOLDER,"suvorovmods")
SERVICEUNITFILE = os.path.expanduser("/usr/lib/systemd/system/suvorov.service")
TXT_FILE_EXTENSIONS = ("txt")
SUV_FILE_EXTENSIONS = ("suv")
DATA_FILE_EXTENSIONS = ("yml","yaml","svy")
