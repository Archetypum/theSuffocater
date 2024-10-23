theSuffocater - ...



Having problems with theSuffocater? Read this article:
    Init Systems:
        - This build uses sysvinit initialization system. If you use systemd, try 'the-suffocater-legacy'.
        
    Notes for BSD users:
        - NetBSD: Ensure that pkgin is installed on NetBSD before running the script. If it’s not available, you may need to install it using the default package manager.
        - OpenBSD: Ensure the necessary packages are available; pfctl is typically included, but you might want to double-check if you need fail2ban.
    
    Common problems with modules:
        - Check if "modules" directory exists && Check if "modules" directory has any .py files.
        - Reinstall theSuffocater from GitHub. Maybe you just have a broken install.
        - Dont change any configurations files and directories unless you know what you are doing.
    
    Current existing bugs:
        idk
        mail me if you found any - industrialmachine2000@protonmail.com
