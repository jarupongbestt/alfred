$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$canonical = Join-Path $root '.codex\skills'
New-Item -ItemType Directory -Force -Path $canonical | Out-Null

foreach ($relativeLink in @('.agents\skills', '.claude\skills')) {
    $linkPath = Join-Path $root $relativeLink
    $parent = Split-Path -Parent $linkPath
    New-Item -ItemType Directory -Force -Path $parent | Out-Null

    if (Test-Path -LiteralPath $linkPath) {
        $existing = Get-Item -Force -LiteralPath $linkPath
        if ($existing.LinkType -eq 'Junction' -and $existing.Target -eq $canonical) {
            Write-Output "Already linked: $relativeLink -> .codex/skills"
            continue
        }
        throw "Path already exists and is not the expected junction: $linkPath"
    }

    New-Item -ItemType Junction -Path $linkPath -Target $canonical | Out-Null
    Write-Output "Created: $relativeLink -> .codex/skills"
}
