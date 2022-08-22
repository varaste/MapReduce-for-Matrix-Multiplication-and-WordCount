<?php
echo "CPU and Memory Intensive";

$myArr = array();
for ($i=0; $i < 1000; $i++){
        for ($j = 0; $j < 500; $j++){
                $myArr[$i] = ($i + $i) + ($j * $j);
        }
}
exec('sudo stress-ng --vm 8 --vm-bytes 32% --timeout 20s');
echo '<pre>'; print_r($myArr); echo '</pre>';
?>