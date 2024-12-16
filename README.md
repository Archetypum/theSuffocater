## theSuffocater  
![Suffocater logo beta 2](https://github.com/user-attachments/assets/51422160-c33c-4515-b628-dbabb2c877ce)

theSuffocater - free open-source extensible module management tool made by
Archetypum that allows you to quickly harden your server and solve your problems
in a few clicks. theSuffocater doesn't require any unix and programming skills
to use it, making it friendly for new users. 
theSuffocater uses sysvinit and init as primary init systems,
but supports ugly fucking systemd, s6, openrc, and launchd as well. 

## Installation (as root):

```
git clone https://github.com/Archetypum/thesuffocater
```

```
cd thesuffocater
```

```
bash requirements.sh
```

```
source pkgenv/bin/activate
```

```
python3 the_suffocater_cli.py
```

theSuffocater is constantly being updated.
Don't forget to

```
git pull origin main
```

to be on the latest version. 

## Usage

Currently, theSuffocater has a small GUI and 11 working modules:

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
 - safe_ssh_setup.py

Hardens your SSH by changing the config file. Essential to your server.
 - tor_management.py

Installs tor, adds tor devuan repositories, setups tor nodes. You know what you're doing.
 - ultimate_firewall.py

Setups firewalls for you using pre-build profiles.
 - user_management.py

Unix user management for new users.
 - usr.py

Most important module to make all others to work properly: simply usr.py is a big list of functions that theSuffocater modules rely on.
 - vpn_server_setup.py

Installs OpenVPN, Wireguard, OutlineVPN and automatically set them up for proper VPN server work.

## Credits

theSuffocater is a project by Archetypum with:
 - Kinderfeld as the lead developer.
(https://github.com/Kinderfeld)
 - wazups as the junior developer, illustrator and GUI maintainer.
(https://github.com/wazups)
 - Mxkxdxnski as the GUI maintainer.
(https://github.com/Mxkxdxnski)
 - NotMakaron as the junior developer and documentation writer.
(https://github.com/NotMakaron)

## Goals

Current goals of theSuffocater:
- Reach 5.0.0-stable version until May.
- Work hard, own nothing, be happy.

## License

theSuffocater uses GNU General Public License V3. 

More information in:

- LICENSE.md
- https://www.fsf.org
- https://www.gnu.org

![gnu](https://github.com/user-attachments/assets/66935a97-374f-4dbc-9f1c-428070fda139)
