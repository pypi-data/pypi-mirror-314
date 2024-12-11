from os import getenv, chdir
import logging
# Use logger that is also in wallman_lib
logger = logging.getLogger("wallman")

try:
    from PIL import Image
except ImportError:
    logging.error("Couldn't import PIL, wallman will launch without a systray.")
    print("Couldn't import PIL, wallman will launch without a systray.")
    raise

try:
    from pystray import Icon, MenuItem as item, Menu
except ImportError:
    logging.error("Couldn't import pystray, wallman will launch without a systray.")
    print("Couldn't import pystray, wallman will launch without a systray.")
    raise

# This should always be ran with "set_wallpaper_by_time" as input!
def set_wallpaper_again(icon, item, wallpaper_setter):
    logging.info("Re-Setting wallpaper due to systray input.")
    wallpaper_setter()

def reroll_wallpapers(icon, item, wallpaper_chooser, wallpaper_setter):
    logging.info("Rerolling Wallpaper sets and resetting wallpaper due to systray input")
    wallpaper_chooser()
    wallpaper_setter()

# This should always be ran with "scheduler.shutdown" as input!
def on_quit(icon, item, shutdown_scheduler):
    logging.info("Shutting down wallman due to systray input.")
    shutdown_scheduler()
    icon.stop()


chdir("/etc/wallman/icons/")
try:
    icon_image = Image.open("systrayIcon.jpg")
except FileNotFoundError:
    logger.error("~/.config/wallman/systrayIcon.jpg has not been found, wallman will launch without a systray.")
    print("~/.config/wallman/systrayIcon.jpg has not been found, wallman will launch without a systray.")
