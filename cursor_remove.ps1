# Cursor Uygulamasını Tamamen Kaldırma Scripti
Write-Host "Cursor IDE kaldırılıyor..." -ForegroundColor Cyan

# 1. Çalışan işlemleri kapat
Get-Process | Where-Object { $_.ProcessName -like "*cursor*" } | ForEach-Object {
    Write-Host "İşlem sonlandırılıyor: $($_.ProcessName)"
    Stop-Process -Id $_.Id -Force
}

# 2. Klasörleri sil
$paths = @(
    "$env:LOCALAPPDATA\Programs\cursor",
    "$env:APPDATA\cursor",
    "$env:USERPROFILE\AppData\Roaming\Cursor",
    "$env:USERPROFILE\Desktop\Cursor.lnk",
    "$env:USERPROFILE\AppData\Local\Cursor",
    "$env:USERPROFILE\AppData\Local\Temp\Cursor"
)

foreach ($path in $paths) {
    if (Test-Path $path) {
        Write-Host "Siliniyor: $path"
        Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# 3. Kayıt defteri girdilerini sil
$regPaths = @(
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall",
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall"
)

foreach ($base in $regPaths) {
    Get-ChildItem $base | Where-Object {
        $_.PSChildName -like "*Cursor*" -or ($_.GetValue("DisplayName") -like "*Cursor*")
    } | ForEach-Object {
        Write-Host "Registry girdisi siliniyor: $($_.PSChildName)"
        Remove-Item -Path $_.PsPath -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# 4. Başlat menüsü ve masaüstü kısayollarını temizle
$shortcuts = @(
    "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\Cursor.lnk",
    "$env:USERPROFILE\Desktop\Cursor.lnk"
)

foreach ($shortcut in $shortcuts) {
    if (Test-Path $shortcut) {
        Write-Host "Kısayol siliniyor: $shortcut"
        Remove-Item -Path $shortcut -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Cursor başarıyla temizlendi ✅" -ForegroundColor Green
Pause
