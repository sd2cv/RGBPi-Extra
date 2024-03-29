from pygame_menu.examples import create_example_window
import pygame
import pygame_menu
import os
import shutil
from RPi import GPIO
from utils import is_raspberrypi
from retroarch_settings import get_retroarch_settings_menu
from rgbpi_tweaks import get_rgbpi_tweaks_menu
from core_updates import get_core_updates_menu
from tweaks_settings import get_tweaks_settings_menu

os.chdir(os.path.dirname(os.path.abspath(__file__)))

RGBPI_UI_ROOT = '/tmp'
SUDOERS_FILE = '/tmp/010_pi-nopasswd'

if is_raspberrypi():
    RGBPI_UI_ROOT = '/opt/rgbpi/ui'
    SUDOERS_FILE = '/etc/sudoers.d/010_pi-nopasswd'

root_enabled = os.path.exists(SUDOERS_FILE)
patch_enabled = os.path.exists(f'{RGBPI_UI_ROOT}/launcher2.pyc')

WINDOW_SIZE = (320, 240)

surface = create_example_window('RGBPi Extra', WINDOW_SIZE, pygame.FULLSCREEN, pygame.JOYAXISMOTION)

pygame.event.set_blocked(pygame.MOUSEMOTION)
pygame.mouse.set_visible(False)

menu_theme = pygame_menu.themes.THEME_DARK.copy()
menu_theme.background_color = (0, 0, 0, 255)
menu_theme.title_offset = (20, 20)
menu_theme.title_font_size = 16
menu_theme.title_font = pygame_menu.font.FONT_MUNRO
menu_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
menu_theme.widget_font_size = 13
menu_theme.widget_font = pygame_menu.font.FONT_MUNRO
menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
menu_theme.scrollbar_color = (0, 0, 0, 255)
menu_theme.scrollbar_slider_color = (0, 0, 0, 255)
menu_theme.scrollbar_thick = (5)

menu = pygame_menu.Menu(
    title='RGBPi Extra v.10a',
    theme=menu_theme,
    joystick_enabled=True,
    width=WINDOW_SIZE[0],
    height=WINDOW_SIZE[1],
    mouse_visible_update=False,
)
#Makes TweaksUI autoclose in 120 seconds
idle_timeout = 960 #seconds
last_input_time = pygame.time.get_ticks()

def toggle_root(value) -> None:
    global last_input_time
    try:
        if value:
            with open(SUDOERS_FILE, 'wt') as f:
                f.write('pi ALL=(ALL) NOPASSWD: ALL')
        else:
            os.remove(SUDOERS_FILE)
        last_input_time = pygame.time.get_ticks()
    except:
        value = not value

def apply_patch():
    global last_input_time
    error = None
    try:
        shutil.move(os.path.join(RGBPI_UI_ROOT, 'launcher.pyc'), os.path.join(RGBPI_UI_ROOT, 'launcher2.pyc'))
        shutil.copy('data/launcher.py', os.path.join(RGBPI_UI_ROOT, 'launcher.py'))
        
        # Copying files from data/tweaks to /opt/rgbpi/ui/tweaks
        shutil.copytree('data/tweaks', os.path.join(RGBPI_UI_ROOT, 'tweaks'), dirs_exist_ok=True)
        
        # Copying files from data/shaders to /root/.config/retroarch/shaders
        shutil.copytree('data/shaders', '/root/.config/retroarch/shaders', dirs_exist_ok=True)
        
        # Copying files from data/cores to /opt/retroarch/cores
        shutil.copytree('data/cores', '/opt/retroarch/cores', dirs_exist_ok=True)
                
        # Append data from data/cores.cfg to /opt/rgbpi/ui/data/cores.cfg
        with open('data/cores.cfg', 'r') as source_file:
            data_to_append = source_file.read()
        with open('/opt/rgbpi/ui/data/cores.cfg', 'r+') as dest_file:
            lines = dest_file.readlines()
            dest_file.seek(0)
            for line in lines:
                if not line.startswith(('melonds_', 'yabasanshiro_')):
                    dest_file.write(line)
            dest_file.write(data_to_append)
            dest_file.truncate()
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        drive = script_dir.split(os.sep)[2]  # Extract the drive from the script path
        media_mountpoint = os.path.join('/', 'media', drive)

        source_dir = os.path.join(os.path.dirname(__file__), 'data', 'drive')
        shutil.copytree(source_dir, media_mountpoint, dirs_exist_ok=True)
        
        with open(os.path.join(RGBPI_UI_ROOT, 'data', 'systems.dat'), 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                file.write(line)
                if line.startswith('"arcade"'):
                    file.write('"atari800","Atari 800",1979,"Atari",".a26|.rom|.zip|.7z|.sh",\n')
                if line.startswith('"sega32x"'):
                    file.write('"saturn","Sega Saturn",1994,"Sega",".cue|.iso|.ccd|.mds|.chd|.sh",\n')
                elif line.startswith('"psx"'):
                    file.write('"psp","Sony PSP",2005,"Sony",".elf|.iso|.cso|.prx|.pbp|.chd|.sh",\n')
                elif line.startswith('"gba"'):
                    file.write('"nds","Nintendo DS",2004,"Nintendo",".nds|.ids|.dsi|.sh",\n')
        
        os.system('reboot')
    except Exception as e:
        import traceback
        traceback.print_exc()
        error = 'patch'
    load_menu(error=error)
    last_input_time = pygame.time.get_ticks()

def load_menu(error=None):
    global last_input_time
    menu.clear()
    if error:
        if error == 'patch':
            menu.add.label('Error applying patch!', wordwrap=False)
        menu.add.vertical_margin(margin=10)
        menu.add.button('OK', load_menu)
    else:
        menu.add.toggle_switch('Root access', root_enabled, toggle_root, width=70, slider_thickness=0, single_click=True, state_text=('disabled', 'enabled'))
        menu.add.vertical_margin(margin=10)
        if not patch_enabled:
            menu.add.button('Apply patch to launcher and reboot', apply_patch)
        else:
            try:
                retroarch_settings_menu = get_retroarch_settings_menu(menu_theme, WINDOW_SIZE)
                rgbpi_tweaks_menu = get_rgbpi_tweaks_menu(menu_theme, WINDOW_SIZE)
                menu.add.button('Retroarch Settings', retroarch_settings_menu)
                menu.add.button('Update Cores', get_core_updates_menu(menu_theme, WINDOW_SIZE))
                menu.add.button('Tweaks', rgbpi_tweaks_menu)
                settings_menu = get_tweaks_settings_menu(menu_theme, WINDOW_SIZE)
                menu.add.button('Settings', settings_menu)
                menu.add.vertical_margin(margin=10)
                menu.add.button('Quit', pygame_menu.events.EXIT)
            except FileNotFoundError:
                menu.add.label('Update Needed! Go to Settings and remove patch', wordwrap=False)
    pygame.display.update()

load_menu()

if __name__ == '__main__':
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)
            current_time = pygame.time.get_ticks()
            if current_time - last_input_time > idle_timeout * 1000:
                exit()
        pygame.display.update()
