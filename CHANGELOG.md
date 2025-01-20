# theSuffocater v2.0.0-stable

This is going to be the REAL second stable release of theSuffocater.
Features CLI and GUI stable versions of theCarcass, new functions, quality of life changes,
and more!

Main changes:
    
    1) Recoded GUI/CLI versions of theCarcass:
        * Added _import_ function.
        * Fixed old functions.
        * Optimised the imports.
        * Many more.
    
    2) Added bash version of theCarcass:

    3) Added bash/python theUnixManager libraries as dependencies:
    
    4) Added _config_files/_ directory:
        * Added _import_py.conf_.
        * Added _import_sh.conf_.       
        * Moved old config files.

    5) Refactored _README.md_ and _CHANGELOG.md_.
        * Now we write markdown much better
    
    6) Improved _requirements.sh_.
        * Removed python requirements installation and added manual instructions.
 
    7) Added _versions/_ directory:
        * Moved theCarcass and theSuffocater versions.
    
    8) Added _requirements/_ directory:
        * Renamed _requirements.sh_ to _install_requirements.sh_ and moved it here.
        * Moved _python_requirements.txt_.

    9) Added _LICENSE-MIT.md_ for VPN install scripts.
    
    11) Refactored and debloated VPN install scripts.

    12) Added _.gitignore_.
    
    *) Minor fixes:
        * Bug files.
        * Removed useless/redundant imports.
        * Typos, spelling mistakes, markdown syntax errors, etc.

"cloc ." statistics:

```text
      54 text files.
      51 unique files.                              
       5 files ignored.

github.com/AlDanial/cloc v 1.96  T=0.03 s (1460.1 files/s, 192098.5 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Bourne Shell                     9            301            158           2303
Python                          16            497            180           1546
Markdown                        10            312              0            937
Text                            16             89              0            387
-------------------------------------------------------------------------------
SUM:                            51           1199            338           5173
-------------------------------------------------------------------------------
```
