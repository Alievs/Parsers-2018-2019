<?php
require("libs\CURL\RollingCurl.class.php");
require("libs\CURL\AngryCurl.class.php");

$file = 'D:\server\OSPanel\domains\parser1.loc\pars_data\data16.txt';
$data = [];
$data = file_get_contents($file);
$urls = unserialize($data);
//echo count($urls);

//foreach ($urls as $ur){
//    echo $ur.'</br>';
//}


//$urls = ['http://www.aldex.com.pl/index.php?route=product/category&path=57_83'];

//for ($i = 1; $i <= 5; $i++) {
//
//    $page = 'http://www.aldex.com.pl/kuchenne?page='. $i;
//    $urls []= $page;
//}

$file2 = 'D:\server\OSPanel\domains\parser1.loc\pars_data\data16.txt';
function request_callback1($response, $info)
{
    global $pages;
    $img='';
    $type_lamp='';
    $type_stl='';
    $color_lamp='';
    $color_stl='';
    $lamp='';
    $socle='';
    $depth='';
    $height='';
    $width='';
    $name='';
    $id='';
    $group='';

//    $products = $xpath->query("//li[contains(@id,'post')]/article/h2/a");//starts-with , contains
//*[contains(text(),'ABC')]

    $doc = new DOMDocument;
    $doc->preserveWhiteSpace = false;
    @$doc->loadHTML($response);
    $xpath = new DOMXPath($doc);
    $line = $xpath->query("//h1");
    $line = $line[0]->nodeValue;
    $mas = explode(' ',$line);
    $id = array_pop($mas);
    $name = implode(' ',$mas);
    $width = $xpath->query("//div[@id='product']/p/strong[1]");
    $width = $width[0]->nodeValue;
    $width = preg_replace("/[^0-9]/", '', $width);
    $depth = $xpath->query("//div[@id='product']/p/strong[2]");
    $depth = $depth[0]->nodeValue;
    $depth = preg_replace("/[^0-9]/", '', $depth);
    $height = $xpath->query("//div[@id='product']/p/strong[3]");
    $height = $height[0]->nodeValue;
    $height = preg_replace("/[^0-9]/", '', $height);
    if ($width == 0){
        $width = '';
    }
    if ($depth == 0){
        $depth = '';
    }
    if ($height == 0){
        $height = '';
    }





    $img_o =  $xpath->query("//ul[@class='thumbnails']/li/a");
    foreach ($img_o as $bow){
        $a = $bow->getAttribute('href');
        $pag [] = $a;
    }
    foreach ($pag as $over){
        $path_to_file = 'C:\Users\игор\Desktop\4wall_4\Aldex\img\\';
        $img  .= 'Aldex_'.basename($over).'|';
        $path = $path_to_file.'Aldex_'.basename($over);
        if(file_exists($path)) { unlink($path); }
        file_put_contents($path, file_get_contents($over));
    }

    $file = 'Aldex.csv';
    $tofile = "$id;$name;$group;;;;;$lamp;$socle;$color_lamp;$type_lamp;$color_stl;$type_stl;$width;$height;$depth;$img\n";
    $bom = "\xEF\xBB\xBF";
    file_put_contents($file, $bom . $tofile . file_get_contents($file));
    unset($pag);

}



$rc = new RollingCurl("request_callback1");
$rc->window_size = 15;

foreach ($urls as $url) {
    $request = new RollingCurlRequest($url);
    $rc->add($request);
}

$rc->execute();

//$result = array_merge($urls, $pages);
//var_dump($result);
//$data = serialize($pages);
//file_put_contents($file2, $data);
//var_dump($pages);
?>