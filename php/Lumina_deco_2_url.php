<?php
require("libs\CURL\RollingCurl.class.php");
require("libs\CURL\AngryCurl.class.php");
//$urls = ['https://skleplamp.pl/KLASYCZNE-c48'];


//запись url-ов в файл

for ($i = 1; $i <= 15; $i++) {

    $page = 'https://centrumswiatla.pl/pl/producer/Lumina-Deco/144/'. $i;
    $urls []= $page;
}


$file1 = 'D:\server\OSPanel\domains\parser1.loc\pars_data\data1.txt';
function request_callback2($response, $info)
{
    global $pages;

//    echo "<hr>";
    $doc = new DOMDocument;
    $doc->preserveWhiteSpace = false;
    @$doc->loadHTML($response);
    $xpath = new DOMXPath($doc);
    $products = $xpath->query("//div[@class='products viewphot s-row']/div/div/a[1]");
    foreach ($products as $row) {
        $pages [] = 'https://centrumswiatla.pl' .$row->getAttribute('href');
    }
}


$rc = new RollingCurl("request_callback2");
$rc->window_size = 15;

foreach ($urls as $url) {
    $request = new RollingCurlRequest($url);
    $rc->add($request);
}

$rc->execute();

//$result = array_merge($urls, $pages);
//var_dump($result);
//$data = serialize($pages);
$comma_separated = implode(" ", $pages);
file_put_contents($file1, $comma_separated);
//var_dump($pages);



?>