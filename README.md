# Reproducing Code

## Downloading vscode
Follow this link to download vscode if you do not have it already installed 

https://code.visualstudio.com/download

## Linking Git to VScode
If you do not have git installed and linked to vscode follow these steps. If you do feel free to ignore this.

1. Download git using this link: https://git-scm.com/install/
2. Type this into your terminal with your name ``` python git config --global user.name "Your Name" ```
3. Type this in your terminal with the email associated to your github ```python git config --global user.email "your.email@example.com"```
4. It should now be linked. If it is not ensure that you have permissions enabled by going to file>settings>permissions in vscode and enable git
It is now setup!

## Copying Repo
1. Follow this link to see our repo https://github.com/BagelSandwich4/2Dminecraft
2. Copy it into your git.
3. Go in vscode and select Clone Git Repository in the center of your screen. If you do not see this you have installed git improperly
4. In the search type 2Dminecraft it should be attached to BagelSandwich4’s git account.
5. Select open the file. 

or type the following command in the terminal
```python
git clone https://github.com/BagelSandwich4/2Dminecraft
```

## Downloading Pygame
If you do not have pygame installed run this command in your terminal when you have cd into the 2Dminecraft directory
```python
pip install -r requirements.txt
```
If this does not work for you you can follow these steps to download pygame 
1. Use this link to download the 1.9.6 version of Pygame. 
	https://www.pygame.org/download.shtml
2. Open the zip file. 
3. Inside you will find a file called setup. Open setup in vscode.
4. Run setup
5. Once it has run pygame should be setup for your computer

# Playing the game:
## Goal:
Defeat the ender dragon by travelling through the overworld, nether and end.
## Controls:
A - move left\
D - move right\
Space - jump\
Number keys - switch through the hotbar slots\
## Picking up items:
You must have an empty slot selected in order to pick up items.\
## Interacting with mobs and blocks.
In order to interact you MUST be holding the correct item.\
Can you find them all?

Start the game by running the file called “minecraft2d.py”\
Have fun!