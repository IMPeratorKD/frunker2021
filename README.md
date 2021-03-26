# frunker2021
A easy 2D game with pygame.

Your target is to surive as lot as possible levels. 
There are n Enemys for each n level. Some of this enemys could be a general. General is faster and has 2 lifes. 
You can move the main rect(you) with "w", "a", "s", "d". There are also two options to kill enemys.
1) By a shot which is created by pressing the Mousebutton. Last position of the shot is the position of your cursor while pressing.(-1 life for enemy; can only kill one enemy)
2) By a knife which can be used three times in a game. To use the knife you should press space button. (-2 lifes for enemys; can kill all enemys nearby)

At the beginning of the match you have 5 lifes. If a enemy touch you, you loose a life and restart the level. With 0 lives you loose the game. Sometimes there is a bonus(ellipse).
Bonus can be earn by you or destroyed by an enemy. Bonus gives you +1 life. 
With tkinter menu you can enter your name and change the color scheme.
