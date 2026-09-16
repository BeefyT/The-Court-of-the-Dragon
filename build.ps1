<#
  build.ps1 - Windows equivalent of the Makefile.

    .\build.ps1          regenerate the codex, then all three PDFs
    .\build.ps1 codex    JSON -> docs\Court-of-the-Dragon-Codex.md
    .\build.ps1 pdf      markdown -> dist\*.pdf
    .\build.ps1 check    verify the codex still matches the JSON
    .\build.ps1 clean    remove generated PDFs
#>
param([string]$Target = "all")

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

$py = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { "python" }

function Invoke-Codex {
    & $py tools\gen_codex.py
    if ($LASTEXITCODE -ne 0) { throw "gen_codex failed" }
}

function Invoke-Pdf {
    $jobs = @(
        @("docs\Court-of-the-Dragon-Codex.md",    "dist\Court-of-the-Dragon-Codex.pdf",     "Court of the Dragon"),
        @("docs\CHANGELOG.md",                    "dist\Court-of-the-Dragon-Changelog.pdf", "Court of the Dragon - Changelog"),
        @("docs\Court-of-the-Dragon-Campaign.md", "dist\Court-of-the-Dragon-Campaign.pdf",  "Court of the Dragon - The Long Hunger")
    )
    foreach ($j in $jobs) {
        & $py tools\mkpdf.py $j[0] $j[1] $j[2]
        if ($LASTEXITCODE -ne 0) { throw "mkpdf failed on $($j[0])" }
    }
}

function Invoke-Check {
    & $py tools\check.py
    if ($LASTEXITCODE -ne 0) { throw "check failed - codex and JSON have drifted" }
}

switch ($Target) {
    "all"   { Invoke-Codex; Invoke-Pdf }
    "codex" { Invoke-Codex }
    "pdf"   { Invoke-Pdf }
    "check" { Invoke-Check }
    "clean" { Remove-Item dist\*.pdf -ErrorAction SilentlyContinue; "cleaned" }
    default { "unknown target '$Target' - use all, codex, pdf, check or clean" }
}
