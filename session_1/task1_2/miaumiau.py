import os

MAGENTA = "\033[38;5;205m"
Teacher = os.environ.get("BESTTEACHER")

if not Teacher:
    print("There is something wrong with your environment variables, please check them.")
else:
    print(MAGENTA + f"""{Teacher} is so proud of you <3.\n""" + r"""
          |
            \     (      /
       `.    \     )    /    .'
         `.   \   (    /   .'
           `.  .-''''-.  .'
     `~._    .'/_    _\`.    _.~'
         `~ /  / \  / \  \ ~'
    _ _ _ _|  _\O/  \O/_  |_ _ _ _
           | (_)  /\  (_) |
        _.~ \  \      /  / ~._
     .~'     `. `.__.' .'     `~.
           .'  `-,,,,-'  `.
         .'   /    )   \   `.
       .'    /    (     \    `.
            /      )     \      
    """)
