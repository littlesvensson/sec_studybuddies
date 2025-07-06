import os

MAGENTA = "\033[38;5;205m"
teacher_path = "/etc/secretinfo/thebestlecturerever"

if not os.path.exists(teacher_path):
    print("There is something wrong with your secret volume, please check it.")
else:
    with open(teacher_path, "r") as f:
        TEACHER = f.read().strip()

    print(MAGENTA + f"""{TEACHER} is so proud of you <3.\n""" + r"""
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
