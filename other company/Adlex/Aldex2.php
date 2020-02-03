<?php
require("libs\CURL\RollingCurl.class.php");
require("libs\CURL\AngryCurl.class.php");


//$urls = ['http://www.aldex.com.pl/index.php?route=product/category&path=57_83'];

for ($i = 1; $i <= 5; $i++) {

    $page = 'http://www.aldex.com.pl/kuchenne?page='. $i;
    $urls []= $page;
}

$file2 = 'D:\server\OSPanel\domains\parser1.loc\pars_data\data16.txt';

function request_callback2($response, $info)
{
    global $pages;

    $doc = new DOMDocument;
    $doc->preserveWhiteSpace = false;
    @$doc->loadHTML($response);
    $xpath = new DOMXPath($doc);
    $products = $xpath->query("//div[@class='product-thumb']/div/a");
    foreach ($products as $row) {
        $pages [] = $row->getAttribute('href');
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
$data = serialize($pages);
file_put_contents($file2, $data);
//var_dump($pages);
?>