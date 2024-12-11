#!/usr/bin/env python3
import wallman_lib

def main():
    validator = wallman_lib.ConfigValidity()
    logic = wallman_lib.WallpaperLogic()
    validator.validate_config()
    logic.set_wallpaper_by_time()
    logic.schedule_wallpapers()

if __name__ == "__main__":
    main()
