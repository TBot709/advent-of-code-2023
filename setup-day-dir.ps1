param (
    [Parameter(Mandatory=$true)]
    [string]$n
)

if (-not $n) {
    Write-Host "no argument, expected day number"
    exit
}

if (-not (Test-Path -Path "day$n")) {
    New-Item -ItemType Directory -Force -Path "day$n"
}

Set-Location -Path "day$n"

Copy-Item -Path "..\day00\day00_template.py" -Destination "day${n}-1.py"
(Get-Content "day${n}-1.py") -replace 'puzzleNumber = "00"', "puzzleNumber = `"$n`"" -replace 'partNumber = "0"', 'partNumber = "1"' | Set-Content "day${n}-1.py"

Copy-Item -Path "..\day00\day00_template.py" -Destination "day${n}-2.py"
(Get-Content "day${n}-2.py") -replace 'puzzleNumber = "00"', "puzzleNumber = `"$n`"" -replace 'partNumber = "0"', 'partNumber = "2"' | Set-Content "day${n}-2.py"

New-Item -ItemType File -Force -Path "day${n}_input.txt"
New-Item -ItemType File -Force -Path "day${n}_example-input.txt"

