<?php
$out=shell_exec("python GetterIndex.py 2 images/nina.jpg 2>&1");
echo $out;
?>
