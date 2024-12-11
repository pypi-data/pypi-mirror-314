[String] $VEnvPath = [IO.Path]::Combine([IO.Path]::GetDirectoryName($PSCommandPath), ".venv")
[String] $SourcePath =  [IO.Path]::GetDirectoryName($PSCommandPath)
$SourcePath += "\."

& "C:/Program Files/Python312/python.exe" -m venv $VEnvPath

[String] $VEnvPythonPath = [IO.Path]::Combine([IO.Path]::GetDirectoryName($PSCommandPath), ".venv", "Scripts/python.exe")
& $VEnvPythonPath -m pip install --upgrade pip
& $VEnvPythonPath -m pip install python-dotenv
& $VEnvPythonPath -m pip install smbprotocol
& $VEnvPythonPath -m pip install pywin32
& $VEnvPythonPath -m pip install paramiko

& $VEnvPythonPath -m pip install $SourcePath
