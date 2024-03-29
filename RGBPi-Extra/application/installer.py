import os
import tarfile
import shutil
import subprocess
import urllib.request
import pygame

def display_loading_screen(screen, font):
    screen.fill(BLACK)
    text_surface = font.render('Downloading RGBPi-Extra', True, WHITE)
    screen.blit(text_surface, (WINDOW_SIZE[0] // 2 - text_surface.get_width() // 2,
                               WINDOW_SIZE[1] // 2 - text_surface.get_height() // 2))
    pygame.display.flip()

pygame.init()
WINDOW_SIZE = (320, 240)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.event.set_blocked(pygame.MOUSEMOTION)
pygame.mouse.set_visible(False)
font = pygame.font.Font(pygame.font.get_default_font(), 14)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

display_loading_screen(screen, font)

repo_owner = "sd2cv"
repo_name = "RGBPi-Extra"
branch = "master"
path = "RGBPi-Extra"

script_dir = os.path.dirname(os.path.abspath(__file__))
archive_url = f"https://github.com/{repo_owner}/{repo_name}/archive/{branch}.tar.gz"
archive_file = os.path.join(script_dir, f"{repo_name}-{branch}.tar.gz")
urllib.request.urlretrieve(archive_url, archive_file)

temp_dir = os.path.join(script_dir, "temp")
os.makedirs(temp_dir, exist_ok=True)
with tarfile.open(archive_file, "r:gz") as tar:
    tar.extractall(path=temp_dir)

source_dir = os.path.join(temp_dir, f"{repo_name}-{branch}", path)
destination_dir = os.path.join(script_dir, path)
if os.path.exists(destination_dir):
    shutil.rmtree(destination_dir)
shutil.move(source_dir, destination_dir)

shutil.rmtree(temp_dir)
os.remove(archive_file)

with subprocess.Popen(['df', '-P', script_dir], stdout=subprocess.PIPE) as proc:
    output = proc.stdout.readlines()
    mount_point = output[1].decode().split()[5]

games_dat = os.path.join(mount_point, 'dats', 'games.dat')

data_to_insert = '"","","ports","ports","/roms/ports/RGBPi-Extra/RGBPi-Extra.sh","RGBPi-Extra","?","?","19XX","1"\n'

with open(games_dat, 'r+') as f:
    lines = f.readlines()
    f.seek(0)
    for line in lines:
        if 'Install RGBPi-Extra.sh' not in line:
            f.write(line)
    f.truncate()

entry_exists = any('RGBPi-Extra.sh' in line for line in open(games_dat, 'r'))
if not entry_exists:
    with open(games_dat, 'a') as f:
        f.write(data_to_insert)

main_script = os.path.join(destination_dir, "application", "main.py")
subprocess.Popen(["python", main_script])

os.remove(__file__)
