$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
$rscriptPath = "C:\Program Files\R\R-4.5.2\bin\Rscript.exe"
$fitScript = Join-Path $scriptDir "03_model_fit.R"

if (-not (Test-Path $rscriptPath)) {
    throw "Rscript.exe was not found at $rscriptPath"
}

& $rscriptPath $fitScript
