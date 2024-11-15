# theSuffocater - extensible module manager that allows you to quickly harden your server and deploy services in few clicks.

# Having problems with theSuffocater? Read this article:

    === Init Systems ===
        - This build uses sysvinit initialization system as primary,
        but supports ugly fucking systemd as well. If you talented
        enough to help me with openrc port, please contact me.
        
    === Notes for BSD users ===
        - *NetBSD*: Ensure that pkgin is installed on NetBSD before
        running requirements.sh. If it’s not available, you may need
        to install it using the default package manager.
        - *OpenBSD*: Ensure the necessary packages are available;
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
    
    === theSuffocater repository navigation ===
        - scripts/: directory for shell scripts.
        Used by the_suffocater_cli.py and the_suffocater_gui.py
	    - modules/: directory for python scripts.
        Used by the_suffocater_cli.py and the_suffocater_gui.py
        - README.md: brief documentation && introduction.    

    === Current goals ===
        - Refactor this ugly piece of shit called README.md
        - Add more really useful modules
        - Make GUI version for idiots
        - Make it support every other geenu slash lenox distos and not just debian and sometimes arch
        - Check how it works on BSD systems
        - Become a better programmer
