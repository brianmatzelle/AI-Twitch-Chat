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
            r"S:\Code May 2023\Chat.tv\blanc32x32.png",
        ],  # Add any additional files, like images, databases, etc.
        "packages": [
            "speech_recognition",
            "PyQt5",
            "six",
            "websocket",
            "websocket_client",
            "pyaudio",
            "openai",
        ],       # Add any additional Python packages needed
    }
}

setup(
    name="Chat.tv",
    version="1.0",
    description="Chat.tv, a fake Live Chat for Twitch.tv streamers",
    options=options,
    executables=executables,
)
