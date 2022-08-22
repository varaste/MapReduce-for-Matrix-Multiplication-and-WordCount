<?php
echo "This is CPU Intensive <br>";
$y=1;
for ($x = 1; $x < 100; $x++) {
        $y = $y * $x;
}
echo "Result of multiplication is: $y <br>";
?>