Enable-WindowsOptionalFeature -Online -FeatureName Containers
Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/microsoft/Windows-Containers/Main/helpful_tools/Install-DockerCE/install-docker-ce.ps1" -o install-docker-ce.ps1
.\install-docker-ce.ps1
docker pull mcr.microsoft.com/windows/servercore:ltsc2019
docker run -d --name powershell-container mcr.microsoft.com/windows/servercore:ltsc2019 powershell -Command "while (`$true) { Start-Sleep -Seconds 3600 }"
