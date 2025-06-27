import os

MAGENTA = "\033[38;5;205m"
THISISME = os.environ.get("IFEELLIKEA", "STUDY BUDDY")

print(MAGENTA + f"""It feels good to be a {THISISME} <3.

      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
    '---''(_/--'  `-'\_)  
""")
