[CmdletBinding()]
param (
    [Parameter(Position = 0)]
    [string]$Path,

    [ValidateSet("prompt", "ts2mp4", "mkv2mp4", "to-mp3", "to-mp4", "compress-mp4", "flac2mp3", "wav2mp3")]
    [string]$Preset = "prompt",

    [string]$OutputDir,

    [switch]$DeleteSource,

    [switch]$Recurse,

    [int]$ThrottleLimit = 4
)

# -----------------------------------------------------------------------------
# Helper: Native Windows Toast Notification
# -----------------------------------------------------------------------------
function Show-Notification {
    param(
        [string]$Title,
        [string]$Message,
        [string]$TargetFolder
    )
    try {
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

        $escapedPath = if ($TargetFolder) { $TargetFolder -replace '\\', '/' } else { "" }
        $template = @"
<toast activationType="protocol" launch="file:///$escapedPath">
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
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("MediaConverter").Show($toast)
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

# -----------------------------------------------------------------------------
# Helper: Locate FFmpeg Binary
# -----------------------------------------------------------------------------
function Get-FFmpegPath {
    $scriptDir = $PSScriptRoot
    $repoRoot = Split-Path -Parent $scriptDir

    $candidates = @(
        (Join-Path $scriptDir "ffmpeg.exe"),
        (Join-Path $repoRoot "ffmpeg.exe"),
        "ffmpeg.exe"
    )

    foreach ($cand in $candidates) {
        if ($cand -eq "ffmpeg.exe") {
            $found = Get-Command "ffmpeg" -ErrorAction SilentlyContinue
            if ($found) { return $found.Source }
        } elseif (Test-Path $cand) {
            return (Resolve-Path $cand).Path
        }
    }
    return "ffmpeg"
}

# -----------------------------------------------------------------------------
# Helper: Robust Clipboard & Explorer Drag/Copy Reader
# -----------------------------------------------------------------------------
function Get-ClipboardMediaTargets {
    $targets = @()

    # 1. Try Explorer copied files (HDROP / FileDropList)
    try {
        Add-Type -AssemblyName System.Windows.Forms
        if ([System.Windows.Forms.Clipboard]::ContainsFileDropList()) {
            $files = [System.Windows.Forms.Clipboard]::GetFileDropList()
            foreach ($f in $files) {
                if (Test-Path $f) { $targets += $f }
            }
        }
    } catch {}

    # 2. Try text path from clipboard
    if ($targets.Count -eq 0) {
        $text = ""
        try {
            Add-Type -AssemblyName System.Windows.Forms
            $text = [System.Windows.Forms.Clipboard]::GetText()
        } catch {}

        if ([string]::IsNullOrWhiteSpace($text)) {
            try {
                $text = (Get-Clipboard 2>$null)
                if ($text -is [array]) { $text = $text -join "`n" }
            } catch {}
        }

        if (-not [string]::IsNullOrWhiteSpace($text)) {
            $lines = $text -split "`r?`n" | ForEach-Object { $_.Trim().Trim('"').Trim("'") } | Where-Object { $_ -ne "" }
            foreach ($line in $lines) {
                if (Test-Path $line) {
                    $targets += (Resolve-Path $line).Path
                }
            }
        }
    }

    return $targets
}

# -----------------------------------------------------------------------------
# Modern Dark Card GUI (WPF XAML)
# -----------------------------------------------------------------------------
if ($Preset -eq "prompt") {
    Add-Type -AssemblyName PresentationFramework, PresentationCore, WindowsBase, System.Windows.Forms

    $clipboardTargets = Get-ClipboardMediaTargets
    $initialPathText = if ($clipboardTargets.Count -gt 0) {
        $clipboardTargets -join "; "
    } elseif (-not [string]::IsNullOrWhiteSpace($Path)) {
        $Path
    } else {
        (Get-Location).Path
    }

    [xml]$xaml = @"
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Media Converter Hub" Height="380" Width="540"
        WindowStartupLocation="CenterScreen" WindowStyle="None" AllowsTransparency="True"
        Background="Transparent" Topmost="True">
    <Window.Resources>
        <ControlTemplate x:Key="DarkComboToggle" TargetType="ToggleButton">
            <Grid>
                <Grid.ColumnDefinitions>
                    <ColumnDefinition />
                    <ColumnDefinition Width="22" />
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
            <Setter Property="FontSize" Value="12"/>
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
                                              Margin="10,2,24,2" VerticalAlignment="Center" HorizontalAlignment="Left">
                                <ContentPresenter.Resources>
                                    <Style TargetType="TextBlock">
                                        <Setter Property="Foreground" Value="#ffffff"/>
                                        <Setter Property="FontWeight" Value="SemiBold"/>
                                    </Style>
                                </ContentPresenter.Resources>
                            </ContentPresenter>
                            <Popup Name="Popup" Placement="Bottom" IsOpen="{TemplateBinding IsDropDownOpen}" AllowsTransparency="True" Focusable="False" PopupAnimation="Slide">
                                <Grid Name="DropDown" SnapsToDevicePixels="True" MinWidth="{TemplateBinding ActualWidth}" MaxHeight="220">
                                    <Border Background="#18181b" BorderThickness="1" BorderBrush="#3f3f46" CornerRadius="4" Margin="0,2,0,0" Padding="3">
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
            <Setter Property="Padding" Value="10,6"/>
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
                <RowDefinition Height="Auto"/> <!-- Title Bar -->
                <RowDefinition Height="Auto"/> <!-- File/Folder Path Row -->
                <RowDefinition Height="Auto"/> <!-- Presets & Config Grid -->
                <RowDefinition Height="Auto"/> <!-- Options Row (Delete source / Recurse) -->
                <RowDefinition Height="*"/>    <!-- Action Buttons -->
            </Grid.RowDefinitions>

            <!-- Title Bar (Draggable) -->
            <Grid Grid.Row="0" Margin="0,0,0,14" Name="TitleBar" Background="Transparent" Cursor="SizeAll">
                <Grid.ColumnDefinitions>
                    <ColumnDefinition Width="*"/>
                    <ColumnDefinition Width="Auto"/>
                </Grid.ColumnDefinitions>
                <StackPanel Orientation="Horizontal" VerticalAlignment="Center">
                    <TextBlock Text="FFmpeg Media Converter" FontSize="15" FontWeight="SemiBold" Foreground="#ffffff"/>
                    <TextBlock Text="  -  Instant Stream Copy &amp; Transcoding" FontSize="11" Foreground="#71717a" VerticalAlignment="Center" Margin="0,1,0,0"/>
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

            <!-- Target Path Box with Browse / Paste Buttons -->
            <Border Grid.Row="1" Background="#18181b" CornerRadius="8" BorderBrush="#27272a" BorderThickness="1" Margin="0,0,0,12" Height="40">
                <Grid Margin="10,0,6,0">
                    <Grid.ColumnDefinitions>
                        <ColumnDefinition Width="*"/>
                        <ColumnDefinition Width="Auto"/>
                        <ColumnDefinition Width="Auto"/>
                    </Grid.ColumnDefinitions>
                    <TextBox Name="TxtPath" Grid.Column="0" Height="30" FontSize="12"
                             Background="Transparent" Foreground="#f4f4f5" BorderThickness="0"
                             VerticalContentAlignment="Center" CaretBrush="#3b82f6"/>
                    <Button Name="BtnBrowse" Grid.Column="1" Content="Browse..." Height="26" Padding="10,0" Margin="4,0"
                            Background="#27272a" Foreground="#a1a1aa" FontSize="11" FontWeight="Medium"
                            BorderThickness="0" Cursor="Hand">
                        <Button.Resources>
                            <Style TargetType="Border">
                                <Setter Property="CornerRadius" Value="4"/>
                            </Style>
                        </Button.Resources>
                    </Button>
                    <Button Name="BtnPaste" Grid.Column="2" Content="Paste" Height="26" Padding="10,0"
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

            <!-- Preset Selection & Details -->
            <Border Grid.Row="2" Background="#18181b" CornerRadius="8" BorderBrush="#27272a" BorderThickness="1" Padding="14,12" Margin="0,0,0,12">
                <Grid>
                    <Grid.RowDefinitions>
                        <RowDefinition Height="Auto"/>
                        <RowDefinition Height="Auto"/>
                    </Grid.RowDefinitions>
                    
                    <Grid Grid.Row="0" Margin="0,0,0,8">
                        <TextBlock Text="Conversion Preset" FontSize="12" FontWeight="SemiBold" Foreground="#60a5fa" VerticalAlignment="Center"/>
                        
                        <ComboBox Name="CmbPreset" HorizontalAlignment="Right" Width="250" Height="28" SelectedIndex="0">
                            <ComboBoxItem Content="TS -> MP4 (Ultra-Fast Remux)" Tag="ts2mp4"/>
                            <ComboBoxItem Content="MKV -> MP4 (Stream Copy)" Tag="mkv2mp4"/>
                            <ComboBoxItem Content="Extract Audio (High Quality MP3)" Tag="to-mp3"/>
                            <ComboBoxItem Content="Universal MP4 (H.264 Re-encode)" Tag="to-mp4"/>
                            <ComboBoxItem Content="Compress Video (CRF 23 Web MP4)" Tag="compress-mp4"/>
                            <ComboBoxItem Content="FLAC -> MP3 (320k)" Tag="flac2mp3"/>
                            <ComboBoxItem Content="WAV -> MP3 (320k)" Tag="wav2mp3"/>
                        </ComboBox>
                    </Grid>

                    <TextBlock Name="TxtPresetDesc" Grid.Row="1"
                               Text="Remuxes MPEG Transport Stream (.ts) to MP4 instantly without re-encoding."
                               FontSize="11" Foreground="#9ca3af" TextWrapping="Wrap"/>
                </Grid>
            </Border>

            <!-- Checkbox Options Row -->
            <Grid Grid.Row="3" Margin="2,0,0,14">
                <Grid.ColumnDefinitions>
                    <ColumnDefinition Width="Auto"/>
                    <ColumnDefinition Width="20"/>
                    <ColumnDefinition Width="Auto"/>
                </Grid.ColumnDefinitions>
                <CheckBox Name="ChkDeleteSource" Grid.Column="0" Content="Delete source files after successful conversion"/>
                <CheckBox Name="ChkRecurse" Grid.Column="2" Content="Scan subdirectories recursively"/>
            </Grid>

            <!-- Execute Button -->
            <Button Name="BtnConvert" Grid.Row="4" Content="Start Conversion" Height="42"
                    Background="#2563eb" Foreground="#ffffff" FontSize="14" FontWeight="SemiBold"
                    BorderThickness="0" Cursor="Hand">
                <Button.Resources>
                    <Style TargetType="Border">
                        <Setter Property="CornerRadius" Value="8"/>
                    </Style>
                </Button.Resources>
            </Button>
        </Grid>
    </Border>
</Window>
"@

    $reader = [System.Xml.XmlNodeReader]::new($xaml)
    $window = [System.Windows.Markup.XamlReader]::Load($reader)

    $titleBar = $window.FindName("TitleBar")
    $titleBar.Add_MouseLeftButtonDown({ $window.DragMove() })

    $btnClose = $window.FindName("BtnClose")
    $btnClose.Add_Click({ $window.Close() })

    $txtPath = $window.FindName("TxtPath")
    $txtPath.Text = $initialPathText

    $btnBrowse = $window.FindName("BtnBrowse")
    $btnBrowse.Add_Click({
        $dialog = New-Object System.Windows.Forms.OpenFileDialog
        $dialog.Title = "Select File or Media"
        $dialog.Filter = "Media Files|*.ts;*.mkv;*.mp4;*.mov;*.flv;*.avi;*.webm;*.flac;*.wav;*.m4a;*.aac|All Files|*.*"
        $dialog.Multiselect = $true
        if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
            $txtPath.Text = ($dialog.FileNames -join "; ")
        }
    })

    $btnPaste = $window.FindName("BtnPaste")
    $btnPaste.Add_Click({
        $cb = Get-ClipboardMediaTargets
        if ($cb.Count -gt 0) {
            $txtPath.Text = ($cb -join "; ")
        }
    })

    $cmbPreset = $window.FindName("CmbPreset")
    $txtDesc = $window.FindName("TxtPresetDesc")
    $chkDelete = $window.FindName("ChkDeleteSource")
    $chkRecurse = $window.FindName("ChkRecurse")
    $btnConvert = $window.FindName("BtnConvert")

    $descriptions = @{
        "ts2mp4"       = "Remuxes MPEG Transport Stream (.ts) to MP4 instantly without re-encoding (-c copy -bsf:a aac_adtstoasc)."
        "mkv2mp4"      = "Remuxes Matroska (.mkv) container to MP4 format instantly via stream copy."
        "to-mp3"       = "Extracts audio stream directly into high-quality VBR MP3 (q:a 0)."
        "to-mp4"       = "Converts any video format into universal compatible H.264 + AAC MP4."
        "compress-mp4" = "Compresses large videos to compact high-quality web MP4 (CRF 23, slow preset)."
        "flac2mp3"     = "Transcodes lossless FLAC audio to 320kbps MP3 with full metadata."
        "wav2mp3"      = "Transcodes uncompressed WAV audio to 320kbps MP3."
    }

    $cmbPreset.Add_SelectionChanged({
        $sel = $cmbPreset.SelectedItem
        if ($sel -and $sel.Tag) {
            $tag = $sel.Tag.ToString()
            if ($descriptions.ContainsKey($tag)) {
                $txtDesc.Text = $descriptions[$tag]
            }
        }
    })

    $script:confirmed = $false
    $btnConvert.Add_Click({
        $script:confirmed = $true
        $script:selectedPath = $txtPath.Text.Trim()
        $sel = $cmbPreset.SelectedItem
        $script:selectedPreset = if ($sel -and $sel.Tag) { $sel.Tag.ToString() } else { "ts2mp4" }
        $script:selectedDelete = [bool]$chkDelete.IsChecked
        $script:selectedRecurse = [bool]$chkRecurse.IsChecked
        $window.Close()
    })

    $window.ShowDialog() | Out-Null

    if (-not $script:confirmed) {
        exit 0
    }

    $Path = $script:selectedPath
    $Preset = $script:selectedPreset
    if ($script:selectedDelete) { $DeleteSource = $true }
    if ($script:selectedRecurse) { $Recurse = $true }
}

# -----------------------------------------------------------------------------
# Input Validation & Target Resolution
# -----------------------------------------------------------------------------
if ([string]::IsNullOrWhiteSpace($Path)) {
    $cb = Get-ClipboardMediaTargets
    if ($cb.Count -gt 0) {
        $rawPaths = $cb
    } else {
        $rawPaths = @((Get-Location).Path)
    }
} else {
    $rawPaths = $Path -split ";" | ForEach-Object { $_.Trim().Trim('"').Trim("'") } | Where-Object { $_ -ne "" }
}

$ffmpeg = Get-FFmpegPath
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " Media Converter Hub (FFmpeg Engine)" -ForegroundColor Cyan
Write-Host " Preset: $Preset | Delete Source: $DeleteSource" -ForegroundColor DarkCyan
Write-Host " FFmpeg Binary: $ffmpeg" -ForegroundColor Gray
Write-Host "==================================================" -ForegroundColor Cyan

# Define extension filter based on preset
$filterExtensions = switch ($Preset) {
    "ts2mp4"       { @(".ts") }
    "mkv2mp4"      { @(".mkv") }
    "to-mp3"       { @(".ts", ".mkv", ".mp4", ".mov", ".flv", ".avi", ".webm", ".m4a", ".wav", ".flac", ".ogg", ".opus") }
    "to-mp4"       { @(".ts", ".mkv", ".mov", ".flv", ".avi", ".webm", ".wmv", ".m4v") }
    "compress-mp4" { @(".mp4", ".mkv", ".mov", ".ts", ".avi", ".webm") }
    "flac2mp3"     { @(".flac") }
    "wav2mp3"      { @(".wav") }
    default        { @(".ts") }
}

# Collect target files
$itemsToProcess = @()
foreach ($rp in $rawPaths) {
    if (Test-Path $rp) {
        $item = Get-Item $rp
        if ($item.PSIsContainer) {
            $gciParams = @{
                Path = $item.FullName
                File = $true
            }
            if ($Recurse) { $gciParams["Recurse"] = $true }
            
            $files = Get-ChildItem @gciParams | Where-Object {
                $ext = $_.Extension.ToLower()
                $filterExtensions -contains $ext
            }
            $itemsToProcess += $files
        } else {
            $ext = $item.Extension.ToLower()
            if ($filterExtensions -contains $ext -or $filterExtensions.Count -eq 0) {
                $itemsToProcess += $item
            }
        }
    }
}

if ($itemsToProcess.Count -eq 0) {
    Write-Warning "No matching media files found for preset '$Preset'."
    Show-Notification -Title "Converter: No Files Found" -Message "No compatible media files found in selected path." -TargetFolder (Get-Location).Path
    exit 0
}

Write-Host "Found $($itemsToProcess.Count) file(s) to process." -ForegroundColor Green

# -----------------------------------------------------------------------------
# FFmpeg Conversion Runner
# -----------------------------------------------------------------------------
$successCount = 0
$failCount = 0
$lastOutputDir = ""
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

foreach ($file in $itemsToProcess) {
    $srcPath = $file.FullName
    $baseName = $file.BaseName
    $srcDir = $file.DirectoryName
    $destDir = if (-not [string]::IsNullOrWhiteSpace($OutputDir)) { $OutputDir } else { $srcDir }

    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }
    $lastOutputDir = $destDir

    # Determine output filename & ffmpeg arguments
    $destExt = switch ($Preset) {
        "to-mp3"   { ".mp3" }
        "flac2mp3" { ".mp3" }
        "wav2mp3"  { ".mp3" }
        default    { ".mp4" }
    }

    $outFileName = "$baseName$destExt"
    # Avoid collision if converting mp4 to compressed mp4 in same folder
    if ($destExt -eq $file.Extension.ToLower() -and $destDir -eq $srcDir) {
        $outFileName = "$baseName.converted$destExt"
    }
    $destPath = Join-Path $destDir $outFileName

    Write-Host "`n>> Processing: $($file.Name)" -ForegroundColor Yellow
    Write-Host "   Target: $destPath" -ForegroundColor DarkGray

    $ffArgs = switch ($Preset) {
        "ts2mp4" {
            # Ultra-fast remux with ADTS to ASC bitstream filter
            @("-nostdin", "-y", "-i", $srcPath, "-c", "copy", "-bsf:a", "aac_adtstoasc", $destPath)
        }
        "mkv2mp4" {
            # Fast container remux
            @("-nostdin", "-y", "-i", $srcPath, "-c", "copy", $destPath)
        }
        "to-mp3" {
            # High-quality VBR MP3 audio extraction
            @("-nostdin", "-y", "-i", $srcPath, "-vn", "-q:a", "0", $destPath)
        }
        "to-mp4" {
            # Universal compatible H.264 + AAC MP4
            @("-nostdin", "-y", "-i", $srcPath, "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-movflags", "+faststart", $destPath)
        }
        "compress-mp4" {
            # High quality compression (CRF 23)
            @("-nostdin", "-y", "-i", $srcPath, "-c:v", "libx264", "-crf", "23", "-preset", "slow", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", $destPath)
        }
        "flac2mp3" {
            # Lossless FLAC to 320k CBR MP3
            @("-nostdin", "-y", "-i", $srcPath, "-c:a", "libmp3lame", "-b:a", "320k", $destPath)
        }
        "wav2mp3" {
            # WAV to 320k CBR MP3
            @("-nostdin", "-y", "-i", $srcPath, "-c:a", "libmp3lame", "-b:a", "320k", $destPath)
        }
        default {
            @("-nostdin", "-y", "-i", $srcPath, "-c", "copy", "-bsf:a", "aac_adtstoasc", $destPath)
        }
    }

    & $ffmpeg @ffArgs

    if ($LASTEXITCODE -eq 0 -and (Test-Path $destPath)) {
        Write-Host "   [OK] Converted successfully." -ForegroundColor Green
        $successCount++

        if ($DeleteSource) {
            Remove-Item -LiteralPath $srcPath -Force
            Write-Host "   [CLEAN] Removed source file: $($file.Name)" -ForegroundColor DarkGray
        }
    } else {
        Write-Host "   [FAIL] FFmpeg exited with code $LASTEXITCODE" -ForegroundColor Red
        $failCount++
    }
}

$stopwatch.Stop()
$elapsedSec = [math]::Round($stopwatch.Elapsed.TotalSeconds, 2)

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host " Conversion Finished in $elapsedSec s" -ForegroundColor Cyan
Write-Host " Success: $successCount | Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Yellow" } else { "Green" })
Write-Host " Output Directory: $lastOutputDir" -ForegroundColor DarkCyan
Write-Host "==================================================" -ForegroundColor Cyan

if ($successCount -gt 0) {
    Show-Notification -Title "Conversion Complete ($successCount file(s))" -Message "Finished in ${elapsedSec}s. Click to view files." -TargetFolder $lastOutputDir
} else {
    Show-Notification -Title "Conversion Failed" -Message "Could not convert target files." -TargetFolder $lastOutputDir
}
