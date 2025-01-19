## theSuffocater  
![Suffocater logo beta 2](https://github.com/user-attachments/assets/51422160-c33c-4515-b628-dbabb2c877ce)

theSuffocater - free open-source extensible module management tool made by
Archetypum that allows you to quickly harden your server, launch services and solve your problems
in a few clicks. theSuffocater doesn't require any Unix and programming skills
to use it, making it friendly for new users. 
theSuffocater uses sysvinit and init as primary init systems,
but supports systemd, s6, openrc, and launchd as well. 

## Installation of theSuffocater-unstable (as root):

```bash
git clone https://github.com/Archetypum/theSuffocater
```

```bash
cd theSuffocater
```

```bash
bash install.sh
```

```bash
python3 -m venv ~/.pkgenv
```

```bash
source ~/.pkgenv/bin/activate
```

```bash
pip install -r install/python_requirements.txt
```

```bash
python3 compile.py
```

## Usage:

CLI launch:

```bash
the_carcass_cli
```

GUI launch:

```bash
the_carcass_gui
```

## Removing theSuffocater (as root):

```bash
bash remove.sh
```

## Credits

theSuffocater is a project by Archetypum with:
 - Kinderfeld as the lead developer and creator.
(https://github.com/Kinderfeld)
 - wazups as the junior developer, illustrator and GUI maintainer.
(https://github.com/wazups)
 - Mxkxdxnski as... tester.
(https://github.com/Mxkxdxnski)
 - WretchOfLights as the junior developer and documentation writer.
(https://github.com/WretchOfLights)

## Goals

Current goals of theSuffocater:
- Reach 5.0.0-stable version until May.
- Work hard, own nothing, be happy.

## Licenses

theSuffocater uses GNU General Public License v3. 

More information in:

- LICENSE.md
- https://www.fsf.org
- https://www.gnu.org

_scripts/openvpn-install.sh_ and _wireguard-install.sh_ by angristan are using MIT Licenses.

More information in:

- LICENSE-MIT.md
- https://mit-license.org/

![gnu](https://github.com/user-attachments/assets/66935a97-374f-4dbc-9f1c-428070fda139)
