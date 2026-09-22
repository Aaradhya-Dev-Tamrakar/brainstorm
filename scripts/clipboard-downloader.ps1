[CmdletBinding()]
param (
    [ValidateSet("prompt", "audio", "video", "mp3", "720p", "1080p")]
    [string]$Mode = "prompt",

    [string]$AudioFormat = "mp3",

    [string]$Quality = "1080p",

    [string]$Url,

    [switch]$Playlist
)

function Update-YtDlpNightly {
    param(
        [string]$YtDlpPath,
        [string]$TargetDir,
        [switch]$Force
    )

    if ([string]::IsNullOrWhiteSpace($YtDlpPath) -or -not (Test-Path $YtDlpPath)) {
        return
    }

    $stampFile = Join-Path $TargetDir ".last_update"
    $needsUpdate = $Force.IsPresent

    if (-not $needsUpdate) {
        if (-not (Test-Path $stampFile)) {
            $needsUpdate = $true
        } else {
            $lastTime = (Get-Item $stampFile).LastWriteTime
            if ((Get-Date) - $lastTime -gt (New-TimeSpan -Hours 24)) {
                $needsUpdate = $true
            }
        }
    }

    if ($needsUpdate) {
        Write-Host "Checking for yt-dlp nightly update..." -ForegroundColor Cyan
        try {
            & $YtDlpPath --update-to nightly
            Set-Content -Path $stampFile -Value (Get-Date -Format "o") -Force
        } catch {
            Write-Warning "Failed to auto-update yt-dlp"
        }
    }
}

function Resolve-CookieArgs {
    param(
        [string]$RepoRoot,
        [string]$ScriptDir
    )

    $localCookies = Join-Path $RepoRoot "cookies.txt"
    if (-not (Test-Path $localCookies)) { $localCookies = Join-Path $ScriptDir "cookies.txt" }

    if (Test-Path $localCookies) {
        return @("--cookies", $localCookies)
    }

    # Browser cookie priority: Edge -> Brave -> Chrome
    $edgeData = Join-Path $env:LOCALAPPDATA "Microsoft\Edge\User Data"
    $braveData = Join-Path $env:LOCALAPPDATA "BraveSoftware\Brave-Browser\User Data"
    $chromeData = Join-Path $env:LOCALAPPDATA "Google\Chrome\User Data"

    if (Test-Path $edgeData) {
        return @("--cookies-from-browser", "edge")
    }
    if (Test-Path $braveData) {
        return @("--cookies-from-browser", "brave")
    }
    if (Test-Path $chromeData) {
        return @("--cookies-from-browser", "chrome")
    }

    return @()
}

# Robust clipboard reading function
function Get-ClipboardUrl {
    $text = ""
    try {
        Add-Type -AssemblyName System.Windows.Forms
        $text = [System.Windows.Forms.Clipboard]::GetText()
    } catch {}

    if ([string]::IsNullOrWhiteSpace($text)) {
        try {
            Add-Type -AssemblyName PresentationCore
            $text = [System.Windows.Clipboard]::GetText()
        } catch {}
    }

    if ([string]::IsNullOrWhiteSpace($text)) {
        try {
            $text = (Get-Clipboard 2>$null)
            if ($text -is [array]) { $text = $text -join "`n" }
        } catch {}
    }

    if ($text) { return $text.Trim() }
    return ""
}

if ([string]::IsNullOrWhiteSpace($Url)) {
    $Url = Get-ClipboardUrl
}

function Show-Notification {
    param(
        [string]$Title,
        [string]$Message,
        [string]$TargetFolder
    )
    try {
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

        $template = @"
<toast activationType="protocol" launch="file:///$($TargetFolder -replace '\\', '/')">
    <visual>
        <binding template="ToastGeneric">
            <text>$Title</text>
            <text>$Message</text>
        </binding>
    </visual>
</toast>
"@
        $xml = [Windows.Data.Xml.Dom.XmlDocument]::new()
        $xml.LoadXml($template)
        $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("DownloaderScripts").Show($toast)
    } catch {
        try {
            Add-Type -AssemblyName System.Windows.Forms
            $balloon = New-Object System.Windows.Forms.NotifyIcon
            $balloon.Icon = [System.Drawing.SystemIcons]::Information
            $balloon.BalloonTipTitle = $Title
            $balloon.BalloonTipText = $Message
            $balloon.Visible = $true
            $balloon.ShowBalloonTip(4000)
        } catch {}
    }
}

# If Mode is prompt, show modern dark card UI
if ($Mode -eq "prompt") {
    Add-Type -AssemblyName PresentationFramework, PresentationCore, WindowsBase

    if ([string]::IsNullOrWhiteSpace($Url)) {
        $Url = Get-ClipboardUrl
    }

    [xml]$xaml = @"
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Downloader Hub" Height="310" Width="510"
        WindowStartupLocation="CenterScreen" WindowStyle="None" AllowsTransparency="True"
        Background="Transparent" Topmost="True">
    <Window.Resources>
        <ControlTemplate x:Key="DarkComboToggle" TargetType="ToggleButton">
            <Grid>
                <Grid.ColumnDefinitions>
                    <ColumnDefinition />
                    <ColumnDefinition Width="20" />
                </Grid.ColumnDefinitions>
                <Border x:Name="Border" Grid.ColumnSpan="2" CornerRadius="4" Background="#27272a" BorderBrush="#3f3f46" BorderThickness="1" />
                <Path x:Name="Arrow" Grid.Column="1" HorizontalAlignment="Center" VerticalAlignment="Center" Data="M 0 0 L 4 4 L 8 0 Z" Fill="#a1a1aa" />
            </Grid>
            <ControlTemplate.Triggers>
                <Trigger Property="IsMouseOver" Value="True">
                    <Setter TargetName="Border" Property="Background" Value="#3f3f46"/>
                </Trigger>
            </ControlTemplate.Triggers>
        </ControlTemplate>

        <Style TargetType="ComboBox">
            <Setter Property="OverridesDefaultStyle" Value="True"/>
            <Setter Property="Foreground" Value="#ffffff"/>
            <Setter Property="FontSize" Value="11"/>
            <Setter Property="FontWeight" Value="SemiBold"/>
            <Setter Property="Template">
                <Setter.Value>
                    <ControlTemplate TargetType="ComboBox">
                        <Grid>
                            <ToggleButton Name="ToggleButton" Template="{StaticResource DarkComboToggle}" Focusable="False"
                                          IsChecked="{Binding Path=IsDropDownOpen, Mode=TwoWay, RelativeSource={RelativeSource TemplatedParent}}"
                                          ClickMode="Press"/>
                            <ContentPresenter Name="ContentSite" IsHitTestVisible="False"
                                              Content="{TemplateBinding SelectionBoxItem}"
                                              ContentTemplate="{TemplateBinding SelectionBoxItemTemplate}"
                                              ContentTemplateSelector="{TemplateBinding ItemTemplateSelector}"
                                              Margin="8,2,20,2" VerticalAlignment="Center" HorizontalAlignment="Left">
                                <ContentPresenter.Resources>
                                    <Style TargetType="TextBlock">
                                        <Setter Property="Foreground" Value="#ffffff"/>
                                        <Setter Property="FontWeight" Value="SemiBold"/>
                                    </Style>
                                </ContentPresenter.Resources>
                            </ContentPresenter>
                            <Popup Name="Popup" Placement="Bottom" IsOpen="{TemplateBinding IsDropDownOpen}" AllowsTransparency="True" Focusable="False" PopupAnimation="Slide">
                                <Grid Name="DropDown" SnapsToDevicePixels="True" MinWidth="{TemplateBinding ActualWidth}" MaxHeight="{TemplateBinding MaxDropDownHeight}">
                                    <Border Background="#18181b" BorderThickness="1" BorderBrush="#3f3f46" CornerRadius="4" Margin="0,2,0,0" Padding="2">
                                        <ScrollViewer SnapsToDevicePixels="True">
                                            <StackPanel IsItemsHost="True" KeyboardNavigation.DirectionalNavigation="Contained" />
                                        </ScrollViewer>
                                    </Border>
                                </Grid>
                            </Popup>
                        </Grid>
                    </ControlTemplate>
                </Setter.Value>
            </Setter>
        </Style>

        <Style TargetType="ComboBoxItem">
            <Setter Property="OverridesDefaultStyle" Value="True"/>
            <Setter Property="Foreground" Value="#f4f4f5"/>
            <Setter Property="Background" Value="#18181b"/>
            <Setter Property="Padding" Value="8,5"/>
            <Setter Property="Cursor" Value="Hand"/>
            <Setter Property="Template">
                <Setter.Value>
                    <ControlTemplate TargetType="ComboBoxItem">
                        <Border Name="ItemBorder" Background="{TemplateBinding Background}" Padding="{TemplateBinding Padding}" CornerRadius="3">
                            <ContentPresenter />
                        </Border>
                        <ControlTemplate.Triggers>
                            <Trigger Property="IsHighlighted" Value="True">
                                <Setter TargetName="ItemBorder" Property="Background" Value="#2563eb"/>
                                <Setter Property="Foreground" Value="#ffffff"/>
                            </Trigger>
                        </ControlTemplate.Triggers>
                    </ControlTemplate>
                </Setter.Value>
            </Setter>
        </Style>

        <Style TargetType="CheckBox">
            <Setter Property="Foreground" Value="#a1a1aa"/>
            <Setter Property="FontSize" Value="11"/>
            <Setter Property="Cursor" Value="Hand"/>
            <Setter Property="Template">
                <Setter.Value>
                    <ControlTemplate TargetType="CheckBox">
                        <StackPanel Orientation="Horizontal" VerticalAlignment="Center">
                            <Border Name="CheckBorder" Width="14" Height="14" CornerRadius="3" Background="#27272a" BorderBrush="#3f3f46" BorderThickness="1" Margin="0,0,7,0">
                                <Path Name="CheckMark" Data="M 2 6 L 5 9 L 10 2" Stroke="#ffffff" StrokeThickness="1.8" Visibility="Collapsed" HorizontalAlignment="Center" VerticalAlignment="Center"/>
                            </Border>
                            <ContentPresenter VerticalAlignment="Center"/>
                        </StackPanel>
                        <ControlTemplate.Triggers>
                            <Trigger Property="IsChecked" Value="True">
                                <Setter TargetName="CheckBorder" Property="Background" Value="#2563eb"/>
                                <Setter TargetName="CheckBorder" Property="BorderBrush" Value="#3b82f6"/>
                                <Setter TargetName="CheckMark" Property="Visibility" Value="Visible"/>
                                <Setter Property="Foreground" Value="#ffffff"/>
                            </Trigger>
                            <Trigger Property="IsMouseOver" Value="True">
                                <Setter TargetName="CheckBorder" Property="BorderBrush" Value="#71717a"/>
                            </Trigger>
                        </ControlTemplate.Triggers>
                    </ControlTemplate>
                </Setter.Value>
            </Setter>
        </Style>
    </Window.Resources>
    <Border Background="#121214" CornerRadius="12" BorderBrush="#27272a" BorderThickness="1">
        <Border.Effect>
            <DropShadowEffect BlurRadius="25" ShadowDepth="4" Opacity="0.6" Color="#000000"/>
        </Border.Effect>
        <Grid Margin="22,16,22,20">
            <Grid.RowDefinitions>
                <RowDefinition Height="Auto"/> <!-- Title & Close Bar -->
                <RowDefinition Height="Auto"/> <!-- URL Box -->
                <RowDefinition Height="Auto"/> <!-- Playlist CheckBox Row -->
                <RowDefinition Height="*"/>    <!-- Cards Grid -->
            </Grid.RowDefinitions>

            <!-- Title Bar (Draggable, pure ASCII) -->
            <Grid Grid.Row="0" Margin="0,0,0,14" Name="TitleBar" Background="Transparent" Cursor="SizeAll">
                <Grid.ColumnDefinitions>
                    <ColumnDefinition Width="*"/>
                    <ColumnDefinition Width="Auto"/>
                </Grid.ColumnDefinitions>
                <StackPanel Orientation="Horizontal" VerticalAlignment="Center">
                    <TextBlock Text="yt-dlp Downloader" FontSize="15" FontWeight="SemiBold" Foreground="#ffffff"/>
                    <TextBlock Text="  -  Auto-Clipboard" FontSize="11" Foreground="#71717a" VerticalAlignment="Center" Margin="0,1,0,0"/>
                </StackPanel>
                <Button Name="BtnClose" Grid.Column="1" Content="X" Width="28" Height="28"
                        Background="#27272a" Foreground="#a1a1aa" FontSize="11" FontWeight="Bold"
                        BorderThickness="0" Cursor="Hand">
                    <Button.Resources>
                        <Style TargetType="Border">
                            <Setter Property="CornerRadius" Value="14"/>
                        </Style>
                    </Button.Resources>
                </Button>
            </Grid>

            <!-- URL Input Container with Paste Button -->
            <Border Grid.Row="1" Background="#18181b" CornerRadius="8" BorderBrush="#27272a" BorderThickness="1" Margin="0,0,0,8" Height="40">
                <Grid Margin="10,0,6,0">
                    <Grid.ColumnDefinitions>
                        <ColumnDefinition Width="*"/>
                        <ColumnDefinition Width="Auto"/>
                    </Grid.ColumnDefinitions>
                    <TextBox Name="TxtUrl" Grid.Column="0" Height="30" FontSize="12"
                             Background="Transparent" Foreground="#f4f4f5" BorderThickness="0"
                             VerticalContentAlignment="Center" CaretBrush="#3b82f6"/>
                    <Button Name="BtnPaste" Grid.Column="1" Content="Paste" Height="26" Padding="10,0"
                            Background="#27272a" Foreground="#a1a1aa" FontSize="11" FontWeight="Medium"
                            BorderThickness="0" Cursor="Hand">
                        <Button.Resources>
                            <Style TargetType="Border">
                                <Setter Property="CornerRadius" Value="4"/>
                            </Style>
                        </Button.Resources>
                    </Button>
                </Grid>
            </Border>

            <!-- Playlist CheckBox Row -->
            <Grid Grid.Row="2" Margin="2,0,0,10">
                <CheckBox Name="ChkPlaylist" Content="Download full playlist (detected in link)" Visibility="Collapsed"/>
            </Grid>

            <!-- Two Action Cards: Audio and Video -->
            <Grid Grid.Row="3">
                <Grid.ColumnDefinitions>
                    <ColumnDefinition Width="*"/>
                    <ColumnDefinition Width="14"/>
                    <ColumnDefinition Width="*"/>
                </Grid.ColumnDefinitions>

                <!-- Audio Card -->
                <Border Grid.Column="0" Background="#18181b" CornerRadius="8" BorderBrush="#27272a" BorderThickness="1" Padding="14,12">
                    <Grid>
                        <Grid.RowDefinitions>
                            <RowDefinition Height="Auto"/>
                            <RowDefinition Height="Auto"/>
                            <RowDefinition Height="*"/>
                        </Grid.RowDefinitions>

                        <Grid Grid.Row="0" Margin="0,0,0,8">
                            <TextBlock Text="Audio Stream" FontSize="12" FontWeight="SemiBold" Foreground="#60a5fa" VerticalAlignment="Center"/>
                            
                            <!-- Custom Dark Formatted ComboBox for Audio -->
                            <ComboBox Name="CmbAudio" HorizontalAlignment="Right" Width="82" Height="26" SelectedIndex="0">
                                <ComboBoxItem Content="MP3"/>
                                <ComboBoxItem Content="FLAC"/>
                                <ComboBoxItem Content="M4A"/>
                                <ComboBoxItem Content="OPUS"/>
                                <ComboBoxItem Content="WAV"/>
                            </ComboBox>
                        </Grid>

                        <TextBlock Grid.Row="1" Text="Embeds cover art &amp; ID3 tags" FontSize="11" Foreground="#71717a" Margin="0,0,0,10"/>

                        <Button Name="BtnAudio" Grid.Row="2" Content="Download Music" Height="38"
                                Background="#2563eb" Foreground="#ffffff" FontSize="13" FontWeight="SemiBold"
                                BorderThickness="0" Cursor="Hand">
                            <Button.Resources>
                                <Style TargetType="Border">
                                    <Setter Property="CornerRadius" Value="6"/>
                                </Style>
                            </Button.Resources>
                        </Button>
                    </Grid>
                </Border>

                <!-- Video Card -->
                <Border Grid.Column="2" Background="#18181b" CornerRadius="8" BorderBrush="#27272a" BorderThickness="1" Padding="14,12">
                    <Grid>
                        <Grid.RowDefinitions>
                            <RowDefinition Height="Auto"/>
                            <RowDefinition Height="Auto"/>
                            <RowDefinition Height="*"/>
                        </Grid.RowDefinitions>

                        <Grid Grid.Row="0" Margin="0,0,0,8">
                            <TextBlock Text="Video Stream" FontSize="12" FontWeight="SemiBold" Foreground="#34d399" VerticalAlignment="Center"/>
                            
                            <!-- Custom Dark Formatted ComboBox for Video -->
                            <ComboBox Name="CmbVideo" HorizontalAlignment="Right" Width="92" Height="26" SelectedIndex="0">
                                <ComboBoxItem Content="1080p"/>
                                <ComboBoxItem Content="4K / Max"/>
                                <ComboBoxItem Content="720p"/>
                                <ComboBoxItem Content="480p"/>
                                <ComboBoxItem Content="360p"/>
                            </ComboBox>
                        </Grid>

                        <TextBlock Grid.Row="1" Text="Direct to Videos\yt-dlp" FontSize="11" Foreground="#71717a" Margin="0,0,0,10"/>

                        <Button Name="BtnVideo" Grid.Row="2" Content="Download Video" Height="38"
                                Background="#059669" Foreground="#ffffff" FontSize="13" FontWeight="SemiBold"
                                BorderThickness="0" Cursor="Hand">
                            <Button.Resources>
                                <Style TargetType="Border">
                                    <Setter Property="CornerRadius" Value="6"/>
                                </Style>
                            </Button.Resources>
                        </Button>
                    </Grid>
                </Border>
            </Grid>
        </Grid>
    </Border>
</Window>
"@

    $reader = [System.Xml.XmlNodeReader]::new($xaml)
    $window = [System.Windows.Markup.XamlReader]::Load($reader)

    $titleBar = $window.FindName("TitleBar")
    $titleBar.Add_MouseLeftButtonDown({
        $window.DragMove()
    })

    $btnClose = $window.FindName("BtnClose")
    $btnClose.Add_Click({
        $window.Close()
    })

    $txtUrl = $window.FindName("TxtUrl")
    $txtUrl.Text = $Url
    if (-not [string]::IsNullOrWhiteSpace($Url)) {
        $txtUrl.SelectAll()
    }

    $btnPaste = $window.FindName("BtnPaste")
    $btnPaste.Add_Click({
        $cb = Get-ClipboardUrl
        if ($cb) {
            $txtUrl.Text = $cb
            $txtUrl.SelectAll()
        }
    })

    $cmbAudio = $window.FindName("CmbAudio")
    $cmbVideo = $window.FindName("CmbVideo")
    $chkPlaylist = $window.FindName("ChkPlaylist")

    $updatePlaylistVisibility = {
        param($currentUrl)
        if ($currentUrl -match '[?&]list=') {
            $chkPlaylist.Visibility = [System.Windows.Visibility]::Visible
            if ($currentUrl -match '(youtube\.com|youtu\.be)/playlist\?') {
                $chkPlaylist.IsChecked = $true
            }
        } else {
            $chkPlaylist.Visibility = [System.Windows.Visibility]::Collapsed
            $chkPlaylist.IsChecked = $false
        }
    }

    $txtUrl.Add_TextChanged({
        & $updatePlaylistVisibility $txtUrl.Text.Trim()
    })

    $window.Add_Loaded({
        $txtUrl.Focus()
        if ([string]::IsNullOrWhiteSpace($txtUrl.Text)) {
            $latest = Get-ClipboardUrl
            if ($latest) { $txtUrl.Text = $latest }
        }
        & $updatePlaylistVisibility $txtUrl.Text.Trim()
    })

    $chosenMode = $null
    $chosenAudioFormat = "mp3"
    $chosenQuality = "1080p"
    $chosenPlaylist = $false

    $btnAudio = $window.FindName("BtnAudio")
    $btnVideo = $window.FindName("BtnVideo")

    $btnAudio.Add_Click({
        $script:chosenMode = "audio"
        $script:Url = $txtUrl.Text.Trim()
        $script:chosenPlaylist = [bool]$chkPlaylist.IsChecked
        $sel = $cmbAudio.SelectedItem
        if ($sel -and $sel.Content) {
            $script:chosenAudioFormat = $sel.Content.ToString().ToLower()
        } else {
            $script:chosenAudioFormat = "mp3"
        }
        $window.Close()
    })

    $btnVideo.Add_Click({
        $script:chosenMode = "video"
        $script:Url = $txtUrl.Text.Trim()
        $script:chosenPlaylist = [bool]$chkPlaylist.IsChecked
        $sel = $cmbVideo.SelectedItem
        $val = "1080p"
        if ($sel -and $sel.Content) {
            $val = $sel.Content.ToString()
        }
        if ($val -match "4K|Max") {
            $script:chosenQuality = "best"
        } elseif ($val -match "720p") {
            $script:chosenQuality = "720p"
        } elseif ($val -match "480p") {
            $script:chosenQuality = "480p"
        } elseif ($val -match "360p") {
            $script:chosenQuality = "360p"
        } else {
            $script:chosenQuality = "1080p"
        }
        $window.Close()
    })

    $window.ShowDialog() | Out-Null

    if (-not $chosenMode) {
        exit 0
    }
    $Mode = $chosenMode
    $AudioFormat = $chosenAudioFormat
    $Quality = $chosenQuality
    if ($chosenPlaylist) { $Playlist = $true }
}

# Validate URL pattern
if ([string]::IsNullOrWhiteSpace($Url) -or ($Url -notmatch "https?://(www\.|music\.)?(youtube\.com|youtu\.be)/.+")) {
    Show-Notification -Title "Downloader: Invalid URL" -Message "Please copy or enter a valid YouTube URL." -TargetFolder "C:\Users\Aaradhya\Music"
    Write-Warning "Not a valid YouTube URL: $Url"
    exit 1
}

# Normalize Mode
if ($Mode -eq "mp3") { $Mode = "audio"; $AudioFormat = "mp3" }
if ($Mode -eq "720p") { $Mode = "video"; $Quality = "720p" }
if ($Mode -eq "1080p") { $Mode = "video"; $Quality = "1080p" }

# Resolve paths
$ScriptDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $ScriptDir

$YtDlp = "yt-dlp"
if (Test-Path (Join-Path $ScriptDir "yt-dlp.exe")) {
    $YtDlp = Join-Path $ScriptDir "yt-dlp.exe"
} elseif (Test-Path (Join-Path $RepoRoot "yt-dlp.exe")) {
    $YtDlp = Join-Path $RepoRoot "yt-dlp.exe"
}

# Auto-update check throttled to every 24 hours
Update-YtDlpNightly -YtDlpPath $YtDlp -TargetDir $RepoRoot

# Resolve cookies (Local cookies.txt first, then Edge, Brave, Chrome fallback)
$cookieArgs = Resolve-CookieArgs -RepoRoot $RepoRoot -ScriptDir $ScriptDir

$DownloadsArchive = Join-Path $RepoRoot "downloads.txt"
if (-not (Test-Path $DownloadsArchive)) { $DownloadsArchive = Join-Path $ScriptDir "downloads.txt" }

# Determine playlist flag: default to --no-playlist unless explicitly confirmed or pure playlist URL
$playlistArgs = @("--no-playlist")
if ($Playlist -or ($Url -match '(youtube\.com|youtu\.be)/playlist\?')) {
    $playlistArgs = @("--yes-playlist")
}

# Destination config
if ($Mode -eq "audio") {
    $TargetFolder = "C:\Users\Aaradhya\Music"
    if (-not (Test-Path $TargetFolder)) { New-Item -ItemType Directory -Path $TargetFolder -Force | Out-Null }

    Show-Notification -Title "Downloading Audio ($AudioFormat)..." -Message "Extracting $AudioFormat and embedding metadata/artwork..." -TargetFolder $TargetFolder

    $argsList = @(
        $cookieArgs +
        $playlistArgs +
        @(
            "--download-archive", $DownloadsArchive,
            "-f", "ba[ext=m4a]/ba",
            "-x",
            "--audio-format", $AudioFormat,
            "--audio-quality", "0",
            "--embed-metadata",
            "--embed-thumbnail",
            "-o", "$TargetFolder\%(playlist_title|Single)s\%(title)s.%(ext)s",
            $Url
        )
    )
} else {
    $TargetFolder = "C:\Users\Aaradhya\Videos\yt-dlp"
    if (-not (Test-Path $TargetFolder)) { New-Item -ItemType Directory -Path $TargetFolder -Force | Out-Null }

    $videoFormat = switch ($Quality) {
        "best"  { "bv*+ba/b" }
        "720p"  { "bv*[ext=mp4][height<=720]+ba[ext=m4a]/b[ext=mp4][height<=720]/b" }
        "480p"  { "bv*[ext=mp4][height<=480]+ba[ext=m4a]/b[ext=mp4][height<=480]/b" }
        "360p"  { "bv*[ext=mp4][height<=360]+ba[ext=m4a]/b[ext=mp4][height<=360]/b" }
        default { "bv*[ext=mp4][height<=1080]+ba[ext=m4a]/b[ext=mp4][height<=1080]/b" }
    }

    Show-Notification -Title "Downloading Video ($Quality)..." -Message "Fetching video stream..." -TargetFolder $TargetFolder

    $argsList = @(
        $cookieArgs +
        $playlistArgs +
        @(
            "--download-archive", $DownloadsArchive,
            "-f", $videoFormat,
            "--merge-output-format", "mp4",
            "--embed-metadata",
            "--embed-thumbnail",
            "-o", "$TargetFolder\%(playlist_title|Single)s\%(title)s.%(ext)s",
            $Url
        )
    )
}

& $YtDlp @argsList

# If failed, attempt a force-update to nightly and retry download once
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Download failed on first attempt. Forcing yt-dlp nightly update and retrying..."
    Update-YtDlpNightly -YtDlpPath $YtDlp -TargetDir $RepoRoot -Force
    & $YtDlp @argsList
}

if ($LASTEXITCODE -eq 0) {
    Show-Notification -Title "Download Complete!" -Message "Saved to $TargetFolder. Click to open." -TargetFolder $TargetFolder
} else {
    Show-Notification -Title "Download Failed" -Message "yt-dlp exited with error code $LASTEXITCODE." -TargetFolder $TargetFolder
}
