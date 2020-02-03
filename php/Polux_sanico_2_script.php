<?php
require("libs\CURL\RollingCurl.class.php");
require("libs\CURL\AngryCurl.class.php");

//запись url-ов в файл

//for ($i = 1; $i <= 2; $i++) {
//
//    $page = 'http://www.argon-lampy.pl/oferta/lampy-stolowe/page/1/'. $i. '/';
//    $urls []= $page;
//}

$urls = ['http://www.sanico.com.pl/nowosci'];

$file1 = 'D:\server\OSPanel\domains\parser1.loc\pars_data\data1.txt';
function request_callback2($response, $info)
{
    global $pages;

    $doc = new DOMDocument;
    $doc->preserveWhiteSpace = false;
    @$doc->loadHTML($response);
    $xpath = new DOMXPath($doc);
    $products = $xpath->query("//nav[@class]/div/a");
    foreach ($products as $row) {
        $pages [] = 'http://www.sanico.com.pl/'.$row->getAttribute('href');
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