<#
.SYNOPSIS
    🛡️ Windows 11 CPU Affinity Shield & Core 0 Isolation Enforcer 🛡️
.DESCRIPTION
    Scans running desktop companion, browser, and mesh processes on Windows 11.
    Strips CPU Core 0 (Bit 0) from process affinity masks and sets process priority
    to BelowNormal so Desktop Window Manager (DWM.exe) and Windows UX never stutter or lag.
.EXAMPLE
    .\apply_win11_safe_affinity.ps1
    .\apply_win11_safe_affinity.ps1 -TargetProcesses "powershell","msedge","python","node"
    .\apply_win11_safe_affinity.ps1 -Watch -IntervalSec 5
#>

[CmdletBinding()]
param (
    [string[]]$TargetProcesses = @("powershell", "pwsh", "msedge", "python", "pythonw", "node"),
    [switch]$Watch,
    [int]$IntervalSec = 5,
    [switch]$VerboseOutput
)

function Audit-And-Apply-Affinity {
    Write-Host ""
    Write-Host "==============================================================================" -ForegroundColor Cyan
    Write-Host " 🛡️ WINDOWS 11 CPU AFFINITY SHIELD • CORE 0 ISOLATION AUDIT" -ForegroundColor Cyan
    Write-Host " Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | Target: ajr-win11-lappy" -ForegroundColor Gray
    Write-Host "==============================================================================" -ForegroundColor Cyan

    $totalCores = [System.Environment]::ProcessorCount
    Write-Host "⚡ Detected Logical Cores: $totalCores" -ForegroundColor DarkCyan

    $results = @()

    foreach ($procName in $TargetProcesses) {
        $procs = Get-Process -Name $procName -ErrorAction SilentlyContinue
        foreach ($proc in $procs) {
            # Filter specifically for companion/mesh or adjust all target executables
            $isMatch = $false
            $cmd = ""
            try {
                $cmd = $proc.CommandLine
            } catch {}

            # Match criteria: Kirby scripts, 8088/win11 edge, or python/node mesh services
            if ($procName -in @("powershell", "pwsh")) {
                if ($cmd -like "*kirby*" -or $cmd -like "*invasion*" -or $proc.MainWindowTitle -like "*Kirby*") {
                    $isMatch = $true
                }
            } elseif ($procName -eq "msedge") {
                if ($cmd -like "*:8088/win11*" -or $proc.MainWindowTitle -like "*Kirby*") {
                    $isMatch = $true
                }
            } else {
                # python or node daemons
                $isMatch = $true
            }

            if (-not $isMatch) { continue }

            try {
                $oldAffinity = $proc.ProcessorAffinity.ToInt64()
                $core0Active = ($oldAffinity -band 1L) -ne 0

                $oldHex = "0x{0:X}" -f $oldAffinity
                $newHex = $oldHex
                $status = "ALREADY_ISOLATED"

                if ($core0Active) {
                    $newAffinity = $oldAffinity -band -bnot 1L
                    if ($newAffinity -gt 0) {
                        $proc.ProcessorAffinity = [System.IntPtr]$newAffinity
                        $newHex = "0x{0:X}" -f $newAffinity
                        $status = "SHIELDED (CORE 0 OFF)"
                    }
                }

                # Set priority to BelowNormal
                if ($proc.PriorityClass -ne [System.Diagnostics.ProcessPriorityClass]::BelowNormal) {
                    try {
                        $proc.PriorityClass = [System.Diagnostics.ProcessPriorityClass]::BelowNormal
                    } catch {}
                }

                $results += [PSCustomObject]@{
                    PID          = $proc.Id
                    Name         = $proc.ProcessName
                    OldAffinity  = $oldHex
                    NewAffinity  = $newHex
                    Priority     = $proc.PriorityClass
                    Core0Status  = "DISABLED (0)"
                    ShieldStatus = $status
                }
            } catch {
                # Process might have exited or requires admin privileges
            }
        }
    }

    if ($results.Count -eq 0) {
        Write-Host "[i] No matching active companion/mesh processes found to shield." -ForegroundColor Yellow
        Write-Host "    (Launch with launch_kirby_win11_safe.bat to spawn shielded instance)" -ForegroundColor Gray
    } else {
        $results | Format-Table -AutoSize
        Write-Host "[✔] Enforced Core 0 Isolation on $($results.Count) process(es). Windows 11 DWM & UX protected!" -ForegroundColor Green
    }
}

# Run initial audit & application
Audit-And-Apply-Affinity

if ($Watch) {
    Write-Host ""
    Write-Host "[*] Watch mode active. Polling every $IntervalSec seconds (Ctrl+C to stop)..." -ForegroundColor Yellow
    while ($true) {
        Start-Sleep -Seconds $IntervalSec
        Audit-And-Apply-Affinity
    }
}
