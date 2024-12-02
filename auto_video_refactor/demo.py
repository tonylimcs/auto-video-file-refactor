from auto_video_refactor.controller.refactor import refactor, preview, exec_refactoring
from auto_video_refactor.controller.cleaner import clean


def main():
    src_dir = input("Source directory: ")
    title = input("Title: ")

    rf_struct = refactor(src_dir, title)
    print(preview(rf_struct))

    if rf_struct:
        confirm = input("\nConfirm? (y/n) ")

        if confirm.lower() == "y":
            exec_refactoring(rf_struct)
            clean(rf_struct)


if __name__ == "__main__":
    main()
