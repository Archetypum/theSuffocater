# theSuffocater v2.0.0-testing

This is going to be the REAL second stable release of theSuffocater, but before that - we need to do some tests.
Features CLI and GUI stable versions of theCarcass, new functions, quality of life changes, and more!

Main changes:
    
1) Recoded GUI/CLI versions of theCarcass:
    * DRY.
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
    
11) Refactored and debloated VPN install scripts.

12) Added _.gitignore_.
    
*) Minor fixes:
    * Bug files.
    * Removed useless/redundant imports.
    * Typos, spelling mistakes, markdown syntax errors, etc.

"cloc ." statistics:

```text
      57 text files.
      54 unique files.                              
      14 files ignored.

github.com/AlDanial/cloc v 1.96  T=0.04 s (1505.2 files/s, 192334.1 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Bourne Shell                     9            317            173           2365
Python                          15            503            205           1550
Markdown                        14            349              0            963
Text                            16             89              0            386
-------------------------------------------------------------------------------
SUM:                            54           1258            378           5264
-------------------------------------------------------------------------------
```
