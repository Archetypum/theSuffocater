# theSuffocater v1.1.9-unstable

This is going to be the second stable release of theSuffocater.
Features CLI and GUI stable versions of the carcass, (more?..) 

Main changes:
    
    1) Improved 'requirements.sh':
        * Added '-h' and '-s' arguments to the parser.
        * Added normal screen cleaning.
        * General polishing and refactoring.

    2) Improved theCarcass:
        * Added 'neofetch' function.
        * Made a better neofetch logo.
        * General polishing and refactoring.

    3) Improved 'usr.py':
        * Just removed it.
    
    4) Added 'community_modules/' directory:
        * Added 'desktop.py' module. Not finished yet.
    
    5) Added latest theUnixManager version to the repo:
        * Removed every 'usr' mentions.
    
    6) Fixed 'tor_management.py':
        * Fixed FreeBSD snowlake-proxy setup process name.
    
    7) Improved 'ssh_management':
        * Renamed 'ssh_key_gen()' to 'ssh_keygen()'.

    *) Minor fixes:
        * Removed useless/redundant imports.
        * Typos, spelling mistakes, markdown syntax errors, etc.

"cloc ." statistics:

```text
      49 text files.
      48 unique files.                              
       3 files ignored.

github.com/AlDanial/cloc v 1.96  T=0.04 s (1269.9 files/s, 198159.0 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                          16            900            528           2943
Bourne Shell                     8            201             34           1207
Markdown                         9            299              0            904
Text                            15             89              0            385
-------------------------------------------------------------------------------
SUM:                            48           1489            562           5439
-------------------------------------------------------------------------------
```
