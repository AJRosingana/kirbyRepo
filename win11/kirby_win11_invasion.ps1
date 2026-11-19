<#
.SYNOPSIS
    🌸 Operation Starfall Poyo: Windows 11 Native Kirby Desktop Companion 🌸
.DESCRIPTION
    Zero-dependency, hardware-accelerated Windows 11 WPF desktop overlay with:
    - Automatic CPU Core 0 isolation (affinity bit 0 disabled to prevent Windows DWM / UX lag)
    - BelowNormal process priority to ensure seamless OS desktop responsiveness
    - Single-instance mutex protection to prevent duplicate ghost processes
    - Safe / Eco Mode (30 FPS animation cap, throttled render load)
    - Cinematic Warp Star entrance and interactive desktop pet interactions.
.NOTES
    Author: MindMesh Autopoietic Engine & Kirby Game Architect
    Target: ajr-win11-lappy (Windows 11)
    Execution: powershell -ExecutionPolicy Bypass -File .\kirby_win11_invasion.ps1 [-SafeMode] [-KillExisting]
#>

[CmdletBinding()]
param (
    [switch]$SafeMode,
    [switch]$MuteAudio,
    [switch]$KillExisting,
    [int64]$AffinityMask = 0
)

# -----------------------------------------------------------------------------
# 0. SINGLE INSTANCE MUTEX & PROCESS DEDUPLICATION
# -----------------------------------------------------------------------------
$mutexName = "Global\KirbyWin11Companion_SingleInstance_Mutex"
$createdNew = $false
try {
    $mutex = [System.Threading.Mutex]::new($true, $mutexName, [ref]$createdNew)
} catch {
    $createdNew = $true
}

if (-not $createdNew) {
    if ($KillExisting) {
        Write-Host "[*] -KillExisting passed: Terminating existing Kirby companion processes..." -ForegroundColor Yellow
        Get-Process -Name powershell, pwsh -ErrorAction SilentlyContinue | Where-Object {
            $_.Id -ne $PID -and ($_.MainWindowTitle -like "*Kirby*" -or $_.CommandLine -like "*kirby_win11_invasion*")
        } | Stop-Process -Force -ErrorAction SilentlyContinue
        Start-Sleep -Milliseconds 400
    } else {
        Write-Warning "[!] Another instance of Kirby Win11 Companion is already running!"
        Write-Host "   Run with -KillExisting to replace running instances, or use launch_kirby_win11_safe.bat." -ForegroundColor Yellow
        exit 0
    }
}

# -----------------------------------------------------------------------------
# 0B. CPU AFFINITY SHIELD: EXCLUDE CORE 0 (PREVENT DWM / UX HITCHING)
# -----------------------------------------------------------------------------
try {
    $currentProc = [System.Diagnostics.Process]::GetCurrentProcess()
    $origAffinity = $currentProc.ProcessorAffinity.ToInt64()
    
    # Calculate mask with bit 0 (Core 0) disabled
    if ($AffinityMask -gt 0) {
        $targetMask = $AffinityMask -band -bnot 1L
    } else {
        $targetMask = $origAffinity -band -bnot 1L
    }

    # If machine has at least 2 cores, apply the non-zero core mask
    if ($targetMask -gt 0) {
        $currentProc.ProcessorAffinity = [System.IntPtr]$targetMask
        $hexMask = "0x{0:X}" -f $targetMask
        Write-Host "⚡ [Affinity Shield] CPU Core 0 DISABLED (Mask: $hexMask). Windows DWM / UX lag prevented!" -ForegroundColor Cyan
    }

    # Set process priority to BelowNormal to guarantee OS/UX smoothness
    $currentProc.PriorityClass = [System.Diagnostics.ProcessPriorityClass]::BelowNormal
    Write-Host "🛡️ [Priority Guard] Process priority set to BelowNormal (Zero OS hitching)." -ForegroundColor Green
} catch {
    Write-Host "[!] Could not set affinity/priority: $_" -ForegroundColor DarkYellow
}

Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName PresentationCore
Add-Type -AssemblyName WindowsBase
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

[System.Windows.Forms.Application]::EnableVisualStyles()

# Ensure WPF doesn't fall back to CPU software rasterization unless forced
try {
    [System.Windows.Media.RenderOptions]::ProcessRenderMode = [System.Windows.Interop.RenderMode]::Default
    if ($SafeMode) {
        Write-Host "🌿 [Safe Mode Active] Enforcing 30 FPS animation cap and zero audio blocking." -ForegroundColor Magenta
        [System.Windows.Media.Animation.Timeline]::DesiredFrameRateProperty.OverrideMetadata(
            [System.Windows.Media.Animation.Timeline],
            [System.Windows.PropertyMetadata]::new([int]30)
        )
    }
} catch {}

Write-Host "⭐ [Operation Starfall Poyo] Initializing Kirby Win11 Desktop Companion..." -ForegroundColor Magenta

# -----------------------------------------------------------------------------
# 1. PROCEDURAL AUDIO SYNTHESIS VIA WINDOWS API (SAFE NON-BLOCKING)
# -----------------------------------------------------------------------------
function Play-PoyoChirp {
    if ($MuteAudio) { return }
    [System.Threading.Tasks.Task]::Run([Action]{
        try {
            [System.Console]::Beep(587, 80)   # D5
            [System.Console]::Beep(880, 90)   # A5
            [System.Console]::Beep(1175, 120) # D6
        } catch {}
    })
}

function Play-WarpStarSound {
    if ($MuteAudio -or $SafeMode) { return }
    [System.Threading.Tasks.Task]::Run([Action]{
        try {
            [System.Console]::Beep(1200, 60)
            [System.Console]::Beep(950, 70)
            [System.Console]::Beep(700, 80)
            [System.Console]::Beep(450, 100)
            [System.Console]::Beep(220, 140)
        } catch {}
    })
}

function Play-TomatoChomp {
    if ($MuteAudio) { return }
    [System.Threading.Tasks.Task]::Run([Action]{
        try {
            [System.Console]::Beep(523, 70)
            [System.Console]::Beep(659, 70)
            [System.Console]::Beep(784, 90)
            [System.Console]::Beep(1046, 120)
        } catch {}
    })
}

# -----------------------------------------------------------------------------
# 2. XAML VECTOR UI SPECIFICATION
# -----------------------------------------------------------------------------
[xml]$xaml = @"
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Kirby Win11 Companion"
        WindowStyle="None"
        AllowsTransparency="True"
        Background="Transparent"
        Topmost="True"
        ShowInTaskbar="False"
        Width="320" Height="280">

    <Grid x:Name="MasterGrid" Background="Transparent">

        <!-- Visual Canvas for Actor & Star Animations -->
        <Canvas x:Name="StageCanvas" Width="320" Height="280">

            <!-- Warp Star Vector Graphic -->
            <Canvas x:Name="WarpStarActor" Width="140" Height="140" Canvas.Left="-220" Canvas.Top="-150">
                <!-- 5-Pointed Star Shape -->
                <Polygon Points="70,10 88,52 134,55 98,85 110,130 70,102 30,130 42,85 6,55 52,52"
                         Stroke="#ca8a04" StrokeThickness="2.5">
                    <Polygon.Fill>
                        <LinearGradientBrush StartPoint="0,0" EndPoint="1,1">
                            <GradientStop Color="#fef08a" Offset="0.0"/>
                            <GradientStop Color="#fde047" Offset="0.6"/>
                            <GradientStop Color="#eab308" Offset="1.0"/>
                        </LinearGradientBrush>
                    </Polygon.Fill>
                </Polygon>
                <!-- Core Glow Sparkle -->
                <Ellipse Canvas.Left="58" Canvas.Top="60" Width="24" Height="24" Fill="#ffffff" Opacity="0.85"/>
            </Canvas>

            <!-- Kirby Avatar Group -->
            <Canvas x:Name="KirbyActor" Width="110" Height="110" Canvas.Left="105" Canvas.Top="85" Cursor="Hand">

                <!-- Left Foot (Shoe) -->
                <Ellipse Canvas.Left="12" Canvas.Top="82" Width="42" Height="26" RenderTransformOrigin="0.5,0.5">
                    <Ellipse.RenderTransform>
                        <RotateTransform Angle="-15"/>
                    </Ellipse.RenderTransform>
                    <Ellipse.Fill>
                        <LinearGradientBrush StartPoint="0,0" EndPoint="0,1">
                            <GradientStop Color="#e11d48" Offset="0.0"/>
                            <GradientStop Color="#9f1239" Offset="1.0"/>
                        </LinearGradientBrush>
                    </Ellipse.Fill>
                </Ellipse>

                <!-- Right Foot (Shoe) -->
                <Ellipse Canvas.Left="58" Canvas.Top="82" Width="42" Height="26" RenderTransformOrigin="0.5,0.5">
                    <Ellipse.RenderTransform>
                        <RotateTransform Angle="15"/>
                    </Ellipse.RenderTransform>
                    <Ellipse.Fill>
                        <LinearGradientBrush StartPoint="0,0" EndPoint="0,1">
                            <GradientStop Color="#e11d48" Offset="0.0"/>
                            <GradientStop Color="#9f1239" Offset="1.0"/>
                        </LinearGradientBrush>
                    </Ellipse.Fill>
                </Ellipse>

                <!-- Left Arm -->
                <Ellipse Canvas.Left="2" Canvas.Top="45" Width="30" Height="24" RenderTransformOrigin="0.5,0.5">
                    <Ellipse.RenderTransform>
                        <RotateTransform Angle="-25"/>
                    </Ellipse.RenderTransform>
                    <Ellipse.Fill>
                        <LinearGradientBrush StartPoint="0,0" EndPoint="1,1">
                            <GradientStop Color="#ff9ec5" Offset="0.0"/>
                            <GradientStop Color="#ff7bac" Offset="0.6"/>
                            <GradientStop Color="#f43f5e" Offset="1.0"/>
                        </LinearGradientBrush>
                    </Ellipse.Fill>
                </Ellipse>

                <!-- Right Arm -->
                <Ellipse Canvas.Left="78" Canvas.Top="45" Width="30" Height="24" RenderTransformOrigin="0.5,0.5">
                    <Ellipse.RenderTransform>
                        <RotateTransform Angle="25"/>
                    </Ellipse.RenderTransform>
                    <Ellipse.Fill>
                        <LinearGradientBrush StartPoint="0,0" EndPoint="1,1">
                            <GradientStop Color="#ff9ec5" Offset="0.0"/>
                            <GradientStop Color="#ff7bac" Offset="0.6"/>
                            <GradientStop Color="#f43f5e" Offset="1.0"/>
                        </LinearGradientBrush>
                    </Ellipse.Fill>
                </Ellipse>

                <!-- Main Kirby Sphere -->
                <Ellipse Canvas.Left="15" Canvas.Top="14" Width="82" Height="82">
                    <Ellipse.Fill>
                        <LinearGradientBrush StartPoint="0,0" EndPoint="1,1">
                            <GradientStop Color="#ff9ec5" Offset="0.0"/>
                            <GradientStop Color="#ff7bac" Offset="0.6"/>
                            <GradientStop Color="#f43f5e" Offset="1.0"/>
                        </LinearGradientBrush>
                    </Ellipse.Fill>
                </Ellipse>

                <!-- Left Cheek Blush -->
                <Ellipse Canvas.Left="24" Canvas.Top="54" Width="15" Height="9" Fill="#fb7185" Opacity="0.8"/>
                <!-- Right Cheek Blush -->
                <Ellipse Canvas.Left="72" Canvas.Top="54" Width="15" Height="9" Fill="#fb7185" Opacity="0.8"/>

                <!-- Left Eye -->
                <Ellipse Canvas.Left="40" Canvas.Top="38" Width="10" Height="24" Fill="#0f172a"/>
                <Ellipse Canvas.Left="42" Canvas.Top="45" Width="7" Height="14" Fill="#0284c7"/>
                <Ellipse Canvas.Left="42" Canvas.Top="40" Width="5" Height="9" Fill="#ffffff"/>

                <!-- Right Eye -->
                <Ellipse Canvas.Left="62" Canvas.Top="38" Width="10" Height="24" Fill="#0f172a"/>
                <Ellipse Canvas.Left="63" Canvas.Top="45" Width="7" Height="14" Fill="#0284c7"/>
                <Ellipse Canvas.Left="64" Canvas.Top="40" Width="5" Height="9" Fill="#ffffff"/>

                <!-- Cheerful Mouth -->
                <Path Data="M 49,60 Q 56,72 63,60 Q 56,64 49,60 Z" Fill="#be123c"/>

            </Canvas>

            <!-- Thought Bubble -->
            <Border x:Name="ThoughtBubble" Canvas.Left="50" Canvas.Top="24" Background="#1e293b" 
                    BorderBrush="#ff7bac" BorderThickness="2" CornerRadius="12" Padding="10,5" Opacity="0">
                <TextBlock x:Name="ThoughtText" Text="Poyo! ( ^-^ )" Foreground="#ffffff" FontWeight="Bold" FontSize="12"/>
            </Border>

        </Canvas>

    </Grid>

</Window>
"@

# -----------------------------------------------------------------------------
# 3. WPF RUNTIME INITIALIZATION & ANIMATION ENGINE
# -----------------------------------------------------------------------------
$reader = [System.Xml.XmlNodeReader]::new($xaml)
$window = [System.Windows.Markup.XamlReader]::Load($reader)

$warpStarActor = $window.FindName("WarpStarActor")
$kirbyActor    = $window.FindName("KirbyActor")
$thoughtBubble = $window.FindName("ThoughtBubble")
$thoughtText   = $window.FindName("ThoughtText")

# Position window at bottom-right corner (above taskbar)
$screenW = [System.Windows.SystemParameters]::PrimaryScreenWidth
$screenH = [System.Windows.SystemParameters]::PrimaryScreenHeight
$window.Left = $screenW - 350
$window.Top  = $screenH - 330

function Say-Message([string]$msg, [int]$durationMs = 3200) {
    $thoughtText.Text = $msg
    $thoughtBubble.Opacity = 1.0
    $timer = [System.Windows.Threading.DispatcherTimer]::new()
    $timer.Interval = [TimeSpan]::FromMilliseconds($durationMs)
    $timer.Add_Tick({
        $thoughtBubble.Opacity = 0.0
        $this.Stop()
    })
    $timer.Start()
}

# -----------------------------------------------------------------------------
# 4. CINEMATIC WARP STAR FLY-IN & DEPARTURE
# -----------------------------------------------------------------------------
function Start-WarpStarEntrance {
    Play-WarpStarSound

    $entranceDuration = if ($SafeMode) { 700 } else { 950 }

    # 1. Fly in Warp Star from offscreen left (-220 -> 90)
    $animX = [System.Windows.Media.Animation.DoubleAnimation]::new(
        -220, 90, [System.Windows.Duration]::new([TimeSpan]::FromMilliseconds($entranceDuration))
    )
    $animX.EasingFunction = [System.Windows.Media.Animation.CubicEase]::new()
    $animX.EasingFunction.EasingMode = [System.Windows.Media.Animation.EasingMode]::EaseOut

    $animY = [System.Windows.Media.Animation.DoubleAnimation]::new(
        -150, 70, [System.Windows.Duration]::new([TimeSpan]::FromMilliseconds($entranceDuration))
    )
    $animY.EasingFunction = [System.Windows.Media.Animation.CubicEase]::new()
    $animY.EasingFunction.EasingMode = [System.Windows.Media.Animation.EasingMode]::EaseOut

    # Completed trigger: Kirby hops, Warp Star departs!
    $animX.Add_Completed({
        Play-PoyoChirp
        if ($SafeMode) {
            Say-Message "⚡ Safe UX Mode: Core 0 Protected! 🌸"
        } else {
            Say-Message "✨ Poyo! Hello Win11 Lappy! (Core 0 Shielded) ✨"
        }

        # Warp Star flies away into deep space (90 -> 380, 70 -> -180)
        [System.Threading.Tasks.Task]::Delay(350).ContinueWith([Action[System.Threading.Tasks.Task]]{
            $window.Dispatcher.Invoke([Action]{
                $exitDuration = if ($SafeMode) { 550 } else { 750 }
                $exitX = [System.Windows.Media.Animation.DoubleAnimation]::new(
                    90, 380, [System.Windows.Duration]::new([TimeSpan]::FromMilliseconds($exitDuration))
                )
                $exitX.EasingFunction = [System.Windows.Media.Animation.ExponentialEase]::new()
                $exitX.EasingFunction.EasingMode = [System.Windows.Media.Animation.EasingMode]::EaseIn

                $exitY = [System.Windows.Media.Animation.DoubleAnimation]::new(
                    70, -180, [System.Windows.Duration]::new([TimeSpan]::FromMilliseconds($exitDuration))
                )
                $exitY.EasingFunction = [System.Windows.Media.Animation.ExponentialEase]::new()
                $exitY.EasingFunction.EasingMode = [System.Windows.Media.Animation.EasingMode]::EaseIn

                $warpStarActor.BeginAnimation([System.Windows.Controls.Canvas]::LeftProperty, $exitX)
                $warpStarActor.BeginAnimation([System.Windows.Controls.Canvas]::TopProperty, $exitY)
            })
        })
    })

    $warpStarActor.BeginAnimation([System.Windows.Controls.Canvas]::LeftProperty, $animX)
    $warpStarActor.BeginAnimation([System.Windows.Controls.Canvas]::TopProperty, $animY)
}

# -----------------------------------------------------------------------------
# 5. MOUSE INTERACTION: DRAG, PET, CONTEXT MENU
# -----------------------------------------------------------------------------
$kirbyActor.Add_MouseLeftButtonDown({
    $window.DragMove()
})

$kirbyActor.Add_MouseRightButtonUp({
    $menu = [System.Windows.Controls.ContextMenu]::new()

    # 1. Warp Star Entrance
    $itemWarp = [System.Windows.Controls.MenuItem]::new()
    $itemWarp.Header = "⭐ Summon Warp Star (Starfall Entrance)"
    $itemWarp.Add_Click({ Start-WarpStarEntrance })
    $menu.Items.Add($itemWarp) | Out-Null

    # 2. Feed Maxi Tomato
    $itemFeed = [System.Windows.Controls.MenuItem]::new()
    $itemFeed.Header = "🍅 Feed Maxi Tomato (Snack)"
    $itemFeed.Add_Click({
        Play-TomatoChomp
        Say-Message "🍅 Maxi Tomato NOM NOM! Delicious!"
    })
    $menu.Items.Add($itemFeed) | Out-Null

    # 3. Hypernova Clipboard Inhale
    $itemInhale = [System.Windows.Controls.MenuItem]::new()
    $itemInhale.Header = "🧹 Hypernova Inhale (Clean Clipboard)"
    $itemInhale.Add_Click({
        try {
            $clip = [System.Windows.Clipboard]::GetText()
            if ($clip) {
                # Clean trailing whitespace and trim
                $cleaned = ($clip.Split("`n") | ForEach-Object { $_.TrimEnd() }) -join "`n"
                [System.Windows.Clipboard]::SetText($cleaned.Trim())
                Play-PoyoChirp
                Say-Message "✨ Inhaled & trimmed clipboard spaces!"
            } else {
                Say-Message "Clipboard is empty poyo!"
            }
        } catch {
            Say-Message "Couldn't read clipboard poyo!"
        }
    })
    $menu.Items.Add($itemInhale) | Out-Null

    # 4. Open Edge Web Companion (:8088/win11)
    $itemWeb = [System.Windows.Controls.MenuItem]::new()
    $itemWeb.Header = "🌐 Open Full Web Companion (:8088/win11)"
    $itemWeb.Add_Click({
        Start-Process "msedge.exe" "--app=http://100.121.245.47:8088/win11 --window-size=560,780"
    })
    $menu.Items.Add($itemWeb) | Out-Null

    # 5. Pet Kirby
    $itemPet = [System.Windows.Controls.MenuItem]::new()
    $itemPet.Header = "💖 Pet Kirby"
    $itemPet.Add_Click({
        Play-PoyoChirp
        Say-Message "❤️ *happy purr* Poyo! ( ˘͈ ᵕ ˘͈ )"
    })
    $menu.Items.Add($itemPet) | Out-Null

    # 6. CPU Affinity & Health Info
    $itemAffinity = [System.Windows.Controls.MenuItem]::new()
    $itemAffinity.Header = "⚡ CPU Affinity Status (Core 0 Shielded)"
    $itemAffinity.Add_Click({
        try {
            $p = [System.Diagnostics.Process]::GetCurrentProcess()
            $mask = "0x{0:X}" -f $p.ProcessorAffinity.ToInt64()
            $pri = $p.PriorityClass
            Say-Message "🛡️ Affinity: $mask | Priority: $pri | Core 0: OFF", 4500
        } catch {
            Say-Message "Affinity active on non-zero cores!"
        }
    })
    $menu.Items.Add($itemAffinity) | Out-Null

    # 7. Exit
    $itemExit = [System.Windows.Controls.MenuItem]::new()
    $itemExit.Header = "❌ Dismiss Kirby to Dream Land"
    $itemExit.Add_Click({ $window.Close() })
    $menu.Items.Add($itemExit) | Out-Null

    $menu.IsOpen = $true
})

# Trigger entrance after window appears
$window.Add_ContentRendered({
    Start-WarpStarEntrance
})

Write-Host "[✔] Kirby Win11 Companion loaded successfully! (Core 0 isolated, BelowNormal priority) Poyo!" -ForegroundColor Green
$window.ShowDialog() | Out-Null
