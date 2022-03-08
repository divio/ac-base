# adds all directories in /app/addons-dev to sys.path
import os
import sys


base_path = os.environ.get('ADDONS_DEV_PATH', '/app/addons-dev')


if os.path.exists(base_path):
    all_directories_in_base_path = next(os.walk(base_path))[1]
    for pkg in sorted(all_directories_in_base_path, reverse=True):
        # sorted in reverse so they end up in alphabetical order (insert(0)
        # reverses the order)
        pkg_dir = os.path.join(base_path, pkg)
        if pkg_dir not in sys.path:
            sys.path.insert(0, pkg_dir)
