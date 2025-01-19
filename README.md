## theSuffocater  
![Suffocater logo beta 2](https://github.com/user-attachments/assets/51422160-c33c-4515-b628-dbabb2c877ce)

theSuffocater - free open-source extensible module management tool made by
Archetypum that allows you to quickly harden your server and solve your problems
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
bash install_requirements.sh
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

CLI launch:

```bash
thesuffocater_cli
```

GUI launch:

```bash
the_suffocater_gui
```

## Removing theSuffocater (as root):

```bash
bash remove.sh
```

## Usage

Currently, theSuffocater has a small GUI, 13 working modules and 6 working scripts:

Modules:

 - passgen.py

Password generator with customizable key length which uses random symbols and random words from user-specified dictionary.
 - address_management.py

Provides MAC address/local IP changing functionality on a unix-like operating systems. 
 - apt_management.py

Provides you all tweaks of the Apt Package Manager on Debian-based
distributions.
 - ip_resolver.py

Resolves Country, city and company of provided IP address.
 - safe_geoclue_setup.py

Disables Geoclue geolocation gathering by changing the config file, improving your OPSEC.
 - ssh_management.py

Hardens your SSH by changing the config file, manages SSH keys and logs connections. Essential to your server.
 - tor_management.py

Installs tor, adds tor devuan repositories, setups tor nodes. You know what you're doing.
 - ultimate_firewall.py

Setups firewalls for you using pre-build profiles.
 - user_management.py

Unix user management for new users.
- fail2ban_setup

Setups fail2ban for you by changing his configurations 
 - vpn_server_setup.py

Installs OpenVPN, Wireguard, OutlineVPN and automatically set them up for proper VPN server work.

Scripts:

 - install_latest_version.sh

Installs the latest version of theSuffocater to your machine. 
 - remove_firmware.sh

Removes binary firmware from your system, making it free.
 - passgen.sh

Password generator with customizable key length which uses random symbols.
 - openvpn_setup.sh

NOT FINISHED YET.
 - wireguard_setup.sh

NOT FINISHED YET.
 - check_ips.sh
NOT FINISHED YET. 

## Credits

theSuffocater is a project by Archetypum with:
 - Kinderfeld as the lead developer and creator.
(https://github.com/Kinderfeld)
 - wazups as the junior developer, illustrator and GUI maintainer.
(https://github.com/wazups)
 - Mxkxdxnski as the GUI helper and tester.
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
