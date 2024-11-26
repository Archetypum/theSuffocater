# theSuffocater - extensible module manager that allows you to quickly harden your server and deploy services in few clicks.

# Installation:
	git clone https://github.com/Kinderfeld/fear-the-suffocater
	cd fear-the-suffocater
	sudo ./requirements.sh
	source pkgenv/bin/activate
	sudo ./the_suffocater_cli.py

# Having problems with theSuffocater? Read this article:
    === Init Systems ===
        - This build uses sysvinit and init as primary init systems, but supports
        ugly fucking systemd, s6, openrc, and launchd as well.
    === Notes for BSD users ===
        - NetBSD: Ensure that pkgin is installed on NetBSD before
        running requirements.sh. If it’s not available, you may need
        to install it using the default package manager.
        - OpenBSD: Ensure the necessary packages are available;
        pfctl is typically included, but you might want to double-check
        if you need fail2ban.
    
    === Common problems with modules ===
        - Check if "modules" directory exists && Check if "modules"
        directory has any .py files.
        - Reinstall theSuffocater using "install_latest_version.sh".
        Maybe you just have a broken installation.
        - Dont change any configurations files and directories unless
        you know what you are doing.
    
    === Current existing bugs ===
        im sorry but the whole suffocater is a one big bug

# Developer? Want to contribute? Read this article:	
	I need people that are smarter than me and can perform:
		- testing on different operating systems and init systems
		- adding more scripts and modules
		- fix bugs
		- make documentation
	
    === Current goals ===
        - Refactor this ugly piece of shit called README.md
        - Add more really useful modules
        - Make GUI version for idiots
        - Check how it works on BSD systems
        - Become a better programmer
