# Auto Video Refactor
Application for refactoring file system structure and filename of video (and subtitle) file.


# Table of Contents

### User Reference
- [Features](#features)
  - [Drag-and-Drop Folder](#drag-and-drop-folder)
  - [Multi-select Folders](#multi-select-folders)
  - [Autosuggest Video Title](#autosuggest-video-title)
  - [Directory Cleanup](#directory-cleanup)
- [Compatibility](#compatibility)
- [Usage](#usage)

### Developer Reference
- [Dependencies](#dependencies)
- [Packaging (.exe)](#packaging-exe)
  - [Method 1](#method-1)
  - [Method 2](#method-2)
- [Maintainability](#maintainability)
- [Future Work](#future-work)

### Disclaimer
- [Credits](#credits)
- [Contributor](#contributor)


---

# <mark>User Reference</mark>


# Features

> ## Drag-and-Drop Folder
> User can drag the source folder(s) and drop directly onto the app window for refactoring.
> 
> ## Multi-select Folders
> User can select multiple source folders if the folders all contain video files of the same TV series.
> 
> > For example, a TV series have 5 seasons, and they are separated into multiple folders, say, 1 folder for each season.
> They can be selected, dragged and dropped onto the app window simultaneously for refactoring. The app will then refactor the file system structure accordingly.
>
> ## Autosuggest Video Title
> The app will try to predict (using simple algorithm) the title of the video by scanning across the source filenames. This feature helps to save the hassle of typing the entire title; moreover, the user only need to make little changes even when the prediction is imperfect.
>
> ## Directory Cleanup
> Source directories will be removed automatically after refactoring, _if they are empty_.


# Compatibility
This app is tested and run on **_Windows 11_**.


# Usage
*Auto Video Refactor* executable (.exe) file can be found in [dist](dist) folder. 
The only file required to run the app.


---

# <mark>Developer Reference</mark>

# Dependencies
- PySide6~=6.8.1
- pyinstaller~=6.11.1 (for packaging into .exe file)


# Maintainability
* All icons should be stored in [icons](auto_video_refactor/view/icons) folder.


# Packaging (.exe)

## Method 1
> First, create the .spec file: \
> <code>pyi-makespec -n 'Auto Video Refactor' --add-data 'auto_video_refactor/view/icons;auto_video_refactor/view/icons' --add-data 'film_roll_icon.ico;.' --icon='film_roll_icon.ico' --windowed --onefile auto_video_refactor.py</code>
> 
> Then, \
> <code>pyinstaller "Auto Video Refactor.spec"</code>
> 
> Subsequently, make edits directly on the .spec file and run *pyinstaller* on this file as the command above.
> 
> Finally, the *dist* folder is created where the .exe file can be found within.

## Method 2
> Run: \
> <code>pyinstaller -n 'Auto Video Refactor' --add-data 'auto_video_refactor/view/icons;auto_video_refactor/view/icons' --add-data 'film_roll_icon.ico;.' --icon='film_roll_icon.ico' --windowed --onefile auto_video_refactor.py</code>
> 
> The .spec file and the *dist* folder are then created; the .exe file can be found in the aforementioned folder.
> 
> Subsequently, make edits directly on the .spec file and run *pyinstaller* on this file like so: \
> <code>pyinstaller "Auto Video Refactor.spec"</code>

#### Reference: [PyInstaller documentations](https://pyinstaller.org/en/stable/usage.html)


# Future Work
- Implement [validation function](auto_video_refactor/controller/validator.py) that will ensure that the output is correct before proceeding to make any changes; trigger errors and warnings to the user when necessary.


---

# <mark>Disclaimer</mark>

# Credits
- Icons for the GUI were taken from [icons8.com](https://icons8.com/icon/set/popular/ultraviolet--static)


# Contributor
### Lim Cheng Siang
> - cslim.careers@gmail.com
> - [GitHub](https://github.com/tonylimcs)
> - [LinkedIn](https://www.linkedin.com/in/tony-lim-cs/)
