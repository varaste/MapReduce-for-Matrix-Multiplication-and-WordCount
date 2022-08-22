<?php
echo "Memory Intensive <br>";
exec('sudo stress-ng --vm 1 --vm-bytes 90% --timeout 120s');
$oo2 = exec('ls -lh');
echo "$oo2 <br>";
$p1 = exec('pwd');
echo "$p1";
?>