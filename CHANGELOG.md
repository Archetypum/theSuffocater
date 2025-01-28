# theSuffocater v2.1.0-stable

REAL second stable release of theSuffocater.
Ladies and Gentleman, Omega and the Mechanical Animals, welcome - this is theSuffocater-v2.1.0-stable!

Features stable theCarcassCLI, unfinished theCarcassGUI and unfinished theCarcass-bash, theUnixManger, new functions,
a lot of bugfixes, documentation, quality of life changes, and more!

BSD port still sucks. Neofetch is unfinished. New MACs and IPs from Address Managenent and not permanent.
theCarcassGUI is unfinished. Tor Management is unfinished. VPN install scripts from angristan are still not rewritten...

...And I don't want to give any promises, but we might change this is the third stable release. 
Now we have much more time to focues on scripts and modules and not on the building libraries and other tSF components.

See you at the end of february!

Main changes:
    
1) Recoded GUI/CLI versions of theCarcass:
    * Added _import_ function.
    * Fixed old functions.
    * Optimised the imports.
    * Many more.
    
2) Added bash version of theCarcass.

3) Added bash/python theUnixManager libraries as dependencies.
    
4) Added _module_configs/_ directory:
    * Added _import_py.conf_.
    * Added _import_sh.conf_.       
    * Moved old config files.

5) Refactored _README.md_ and _CHANGELOG.md_.
    * Now we write markdown much better.
    
6) Improved _requirements_installer.sh_:
    * Removed python requirements installation and added manual instructions.
 
7) Added _versions/_ directory:
    * Moved theCarcass and theSuffocater versions.
    
8) Added _requirements/_ directory:
    * Renamed _requirements.sh_ to _install_requirements.sh_ and moved it here.
    * Moved _python_requirements.txt_.

9) Added _LICENSE-MIT.md_ for VPN install scripts.
    
10) Added _.gitignore_.

11) Added _tsf_installer.sh_:
    * Added _debug_ function.
    * Added parsing functionality.

12) Added automatic imports to theCarcass:
    * Added _import_py.conf_ and _import_sh.conf_ for it.

13) Added _AUTHORS.md_.

14) Improved documentation.

*) Minor fixes:
    * DRY.
    * Bug fixes.
    * Removed useless/redundant imports.
    * Typos, spelling mistakes, Markdown syntax errors, etc.

"cloc ." statistics:

```text
      59 text files.
      55 unique files.                              
      19 files ignored.

github.com/AlDanial/cloc v 1.96  T=0.04 s (1357.4 files/s, 193642.1 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Bourne Shell                     9            333            188           2426
Python                          15            694            515           1855
Markdown                        15            367              0            993
Text                            16             89              0            386
-------------------------------------------------------------------------------
SUM:                            55           1483            703           5660
-------------------------------------------------------------------------------
```
