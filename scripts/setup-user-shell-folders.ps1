<#
.SYNOPSIS
    Applies and restores Windows User Shell Folders configuration.
.DESCRIPTION
    Configures customized user shell paths (such as Images, Screenshots, OneDrive documents, Desktop, Downloads, etc.)
    under HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders.
#>

[CmdletBinding()]
param(
    [switch]$Force
)

$registryPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"

$shellFolders = [ordered]@{
    "AppData"                                  = "%USERPROFILE%\AppData\Roaming"
    "Cache"                                    = "%USERPROFILE%\AppData\Local\Microsoft\Windows\INetCache"
    "Cookies"                                  = "%USERPROFILE%\AppData\Local\Microsoft\Windows\INetCookies"
    "Desktop"                                  = "C:\Users\Aaradhya\OneDrive\Desktop"
    "Favorites"                                = "%USERPROFILE%\Favorites"
    "History"                                  = "%USERPROFILE%\AppData\Local\Microsoft\Windows\History"
    "Local AppData"                            = "%USERPROFILE%\AppData\Local"
    "My Music"                                 = "%USERPROFILE%\Music"
    "My Pictures"                              = "%USERPROFILE%\Images"
    "My Video"                                 = "%USERPROFILE%\Videos"
    "NetHood"                                  = "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Network Shortcuts"
    "Personal"                                 = "C:\Users\Aaradhya\OneDrive\Documents"
    "PrintHood"                                = "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Printer Shortcuts"
    "Programs"                                 = "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
    "Recent"                                   = "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Recent"
    "SendTo"                                   = "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\SendTo"
    "Start Menu"                               = "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu"
    "Startup"                                  = "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    "Templates"                                = "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Templates"
    "{374DE290-123F-4565-9164-39C4925E467B}"  = "%USERPROFILE%\Downloads"
    "{F42EE2D3-909F-4907-8871-4C22FC0BF756}"  = "C:\Users\Aaradhya\OneDrive\Documents"
    "{0DDD015D-B06C-45D5-8C4C-F59713854639}"  = "%USERPROFILE%\Images"
    "{B7BEDE81-DF94-4682-A7D8-57A52620B86F}"  = "%USERPROFILE%\Images\Screenshots"
}

Write-Host "Applying User Shell Folders configuration..." -ForegroundColor Cyan

foreach ($entry in $shellFolders.GetEnumerator()) {
    $name = $entry.Key
    $value = $entry.Value
    
    # Ensure target directory exists if expandable
    $expandedPath = [System.Environment]::ExpandEnvironmentVariables($value)
    if (-not (Test-Path -Path $expandedPath)) {
        try {
            New-Item -ItemType Directory -Path $expandedPath -Force | Out-Null
            Write-Host "  [+] Created directory: $expandedPath" -ForegroundColor Green
        } catch {
            Write-Warning "  [!] Could not create directory: $expandedPath ($_)"
        }
    }

    Set-ItemProperty -Path $registryPath -Name $name -Value $value -Type ExpandString
    Write-Host "  [*] Set $name -> $value" -ForegroundColor Gray
}

Write-Host "`nUser Shell Folders applied successfully." -ForegroundColor Green
Write-Host "Note: Restart Explorer (Stop-Process -Name explorer -Force) to apply changes system-wide." -ForegroundColor Yellow
