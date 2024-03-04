# Fake Powershell
Have you ever wanted a fake powershell? Well now you can!

Python Tkinter GUI connects to a Windows Server 2019 docker container running powershell. These commands are passed back to the GUI so the user may not catch on that they typing into in a container.

The main powershell can be found at `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`, so use that if your powershell PATH becomes messed up.

# Setup
1. Run `install_docker.ps1` script to install docker on Windows Server 2019.

2. Run `install_fake_powershell.ps1` to download `script.exe` and `powershell.ico` to `C:/Program Files/Fake PowerShell`

3. Run `remove_shortcuts.ps1` to remove the existing powershell shorcuts, so they no longer appear in the search results

4. Run `put_shortcuts_back.ps1` to put the shortcuts back, and have powershell appear in the search results once again

# Compilation
Just compile it on windows ok. It is classified as malware, so you may want to turn your antivirus off when compiling.

With many thanks to my friend Ron for compiling it on his machine.

**The current exe file requires powershell.ico to be in its directory**

1. Install python from the web. Also can install [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)
2. `py -m pip install pyinstaller`
3. `py -m PyInstaller --onefile --windowed --icon=powershell.ico --add-data "powershell.ico;." script.py`
