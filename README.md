theSuffocater - extensible module manager that allows you to
quickly harden your server and deploy services in few clicks.

Having problems with theSuffocater? Read this article:

    === Init Systems ===
        - This build uses sysvinit initialization system. If you use systemd,
          try 'the-suffocater-legacy'. Unfortunately we dont have openrc build yet.
        
    === Notes for BSD users ===
        - *NetBSD*: Ensure that pkgin is installed on NetBSD before running the script. If it’s not
          available, you may need to install it using the default package manager.
        - *OpenBSD*: Ensure the necessary packages are available; pfctl is typically included,
          but you might want to double-check if you need fail2ban.
    
    === Common problems with modules ===
        - Check if "modules" directory exists && Check if "modules" directory has any .py files.
        - Reinstall theSuffocater from GitHub. Maybe you just have a broken install.
        - Dont change any configurations files and directories unless you know what you are doing.
    
    === Current existing bugs ===
        idk
        mail me if you found any - industrialmachine2000@protonmail.com


Developer? Want to contribute? Read this article:
    
    === theSuffocater repository navigation ===
        - (blahblahblah)

    === Current goals ===
        - Refactor this ugly piece of shit called README.md
        - Add more really useful modules
        - Make GUI version for idiots
        - Make it support every other geenu slash lenox and not just debian
        - Check how it works on BSD systems
        - Become a better programmer
