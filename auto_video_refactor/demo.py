from controller.refactor import refactor, exec_refactoring

import common
import os


def main():
    src_dir = r"C:\Users\Lim Cheng Siang\Downloads\Attack on Titan (2013)"

    title = "Attack on Titan (2013)"

    _dict = refactor(src_dir, title)

    if _dict:
        _input = input("\nConfirm? (y/n) ")
        _input = 'y'

        if _input.lower() == "y":
            exec_refactoring(_dict)

            if src_dir != str(os.path.join(os.path.dirname(src_dir), title)):
                common.remove_dir(src_dir)


if __name__ == "__main__":
    main()
