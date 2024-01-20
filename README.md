# Fake Powershell
Have you ever wanted a fake powershell? Well now you can!

Python Tkinter GUI connects to a Windows Server 2019 docker container running powershell. These commands are passed back to the GUI so the user may not catch on that they are in a container.

Run the `install_docker.ps1` script to install docker on Windows Server 2019.

# Compilation
Just compile it on windows ok. It is classified as malware, so you may want to turn your antivirus off when compiling.

With many thanks to my friend Ron for compiling it on his machine.

**The current exe file requires powershell.ico to be in its directory**

1. Install python from the web. Also can install [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)
2. `py -m pip install pyinstaller`
3. `py -m PyInstaller --onefile --windowed --icon=powershell.ico --add-data "powershell.ico;." script.py`
