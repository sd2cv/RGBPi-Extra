import os
import shutil
import pygame_menu
import subprocess
import glob
import sys 

# Define the root directory of the RGB-Pi UI
RGBPI_UI_ROOT = '/opt/rgbpi/ui'

def remove_patch():
    error = None

    # Define the paths for launcher.py, launcher2.pyc, tweaks folder
    launcher_py_path = os.path.join(RGBPI_UI_ROOT, 'launcher.py')
    launcher_pyc_path = os.path.join(RGBPI_UI_ROOT, 'launcher.pyc')
    launcher2_pyc_path = os.path.join(RGBPI_UI_ROOT, 'launcher2.pyc')
    tweaks_folder_path = os.path.join(RGBPI_UI_ROOT, 'tweaks')

    # Function to handle renaming launcher2.pyc to launcher.pyc
    def rename_launcher_pyc():
        try:
            os.rename(launcher2_pyc_path, launcher_pyc_path)
        except Exception as e:
            import traceback
            traceback.print_exc()
            error = 'patch'

    # Function to remove system entries from dat file
    def remove_system_entries(dat_file_path):
        try:
            with open(dat_file_path, 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    if not any(system in line for system in ['nds', 'psp', 'saturn', 'atari800']):
                        file.write(line)
                file.truncate()
        except Exception as e:
            import traceback
            traceback.print_exc()
            error = 'patch'

    # Remove launcher.py, rename launcher2.pyc to launcher.pyc, delete tweaks folder
    try:
        # Remove launcher.py if it exists
        if os.path.exists(launcher_py_path):
            os.remove(launcher_py_path)

        # Rename launcher2.pyc to launcher.pyc if it exists
        if os.path.exists(launcher2_pyc_path):
            rename_launcher_pyc()

        # Delete the tweaks folder if it exists
        if os.path.exists(tweaks_folder_path):
            shutil.rmtree(tweaks_folder_path)

    except Exception as e:
        import traceback
        traceback.print_exc()
        error = 'patch'

    # Define the fixed paths for games.dat, favorites.dat, and systems.dat
    games_dat_path = '/media/*/dats/games.dat'
    favorites_dat_path = '/media/*/dats/favorites.dat'
    systems_dat_path = '/opt/rgbpi/ui/data/systems.dat'

    # Remove system entries from games.dat
    games_dat_files = glob.glob(games_dat_path)
    for file_path in games_dat_files:
        remove_system_entries(file_path)

    # Remove system entries from favorites.dat
    favorites_dat_files = glob.glob(favorites_dat_path)
    for file_path in favorites_dat_files:
        remove_system_entries(file_path)

    # Remove system entries from systems.dat
    remove_system_entries(systems_dat_path)

    # Reboot system
    os.system('reboot')

def update_and_restart():
    # Run updater.py in a separate process
    subprocess.Popen(['python', 'updater.py'])
    
    # Terminate the current process running the Pygame UI
    sys.exit()
    
def get_tweaks_settings_menu(menu_theme, WINDOW_SIZE):
    menu = pygame_menu.Menu(
        title='',
        theme=menu_theme,
        joystick_enabled=True,
        width=WINDOW_SIZE[0],
        height=WINDOW_SIZE[1],
        mouse_visible_update=False,
    )

    menu.add.button('Update to latest version', update_and_restart)
    menu.add.button('Remove Patch and Reboot (This removes all tweaks)', remove_patch)
    menu.add.button('Return to menu', pygame_menu.events.BACK)

    return menu