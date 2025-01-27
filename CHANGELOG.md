# theSuffocater v2.0.0-testing

This is going to be the REAL second stable release of theSuffocater, but before that - we need to do some tests.
Features CLI and GUI stable versions of theCarcass, new functions, quality of life changes, and more!

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

*) Minor fixes:
    * DRY.
    * Bug fixes.
    * Removed useless/redundant imports.
    * Typos, spelling mistakes, Markdown syntax errors, etc.

"cloc ." statistics:

```text
      58 text files.
      54 unique files.                              
      20 files ignored.

github.com/AlDanial/cloc v 1.96  T=0.04 s (1257.2 files/s, 168750.0 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Bourne Shell                     9            326            176           2416
Python                          15            573            313           1645
Markdown                        14            353              0            971
Text                            16             89              0            386
-------------------------------------------------------------------------------
SUM:                            54           1341            489           5418
-------------------------------------------------------------------------------
```
