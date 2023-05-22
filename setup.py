from cx_Freeze import setup, Executable

# Replace 'your_script_name' with the name of your Python script without the .py extension
executables = [Executable(r"S:\Code May 2023\Chat.tv\main.py", 
    icon=r"S:\Code May 2023\Chat.tv\blanc.ico",
    shortcut_name="Chat.tv",
    base="Win32GUI"
)]

options = {
    "build_exe": {
        "include_files": [
            # any additional files, like images, databases, etc.
            r"S:\Code May 2023\Chat.tv\blanc32x32.png",
            r"S:\Code May 2023\Chat.tv\blanc.png",
            r"S:\Code May 2023\Chat.tv\blanc.ico",
        ], 
        "packages": ["os"], "excludes": ["tkinter"]
    }
}

setup(
    name="Chat.tv",
    version="0.1.4",
    description="Chat.tv, a fake Live Chat for Twitch.tv streamers",
    options=options,
    executables=executables,
)
