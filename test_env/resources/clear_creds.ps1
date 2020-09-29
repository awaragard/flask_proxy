

foreach ($m in (cmdkey /list) -match "Target:"){

    $m = $m.Replace("Target:","").Trim()
    Write-Host "Removing " $m
    cmdkey /delete $m

}
