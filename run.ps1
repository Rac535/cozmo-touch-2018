$currentDirectory = (Get-Item -Path ".\").FullName
$env:Path += ";$currentDirectory\platform-tools"
"Loading..."
./dist/main.exe
Read-Host -Prompt "Press Enter to exit"
