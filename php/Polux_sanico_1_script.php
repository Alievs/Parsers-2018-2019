<?php
require("libs\CURL\RollingCurl.class.php");
require("libs\CURL\AngryCurl.class.php");


//чтение url-ов из файла
$file = 'D:\server\OSPanel\domains\parser1.loc\pars_data\datall.txt';
$data = [];
$data = file_get_contents($file);
$urls = explode(" ", $data);
//$urls = unserialize($data);
//echo count($urls);

//foreach ($urls as $ur){
//    echo $ur.'</br>';
//}

//$urls = ['http://www.sanico.com.pl/sanico-termowentylator-fh-202-b4-czarny',
//    'http://www.sanico.com.pl/probus-led-39w-2500lm'];

//for ($i = 1; $i <= 5; $i++) {
//
//    $page = 'http://www.aldex.com.pl/kuchenne?page='. $i;
//    $urls []= $page;
//}

$file2 = 'D:\server\OSPanel\domains\parser1.loc\pars_data\data2.txt';
function request_callback1($response, $info)
{
    global $pages;
    $id='';
    $name='';
    $group='';
    $style='';
    $lamp='';
    $socle='';
    $color_lamp='';
    $type_lamp='';
    $color_stl='';
    $type_stl='';
    $depth='';
    $height='';
    $width='';
    $img='';

    $doc = new DOMDocument;
    $doc->preserveWhiteSpace = false;
    @$doc->loadHTML($response);
    $xpath = new DOMXPath($doc);
//    [contains(.,'trzonek:')]

    $id = $xpath->query("//div[@id='parameters']/div[contains(.,'index')]");
    $id = $id[0]->nodeValue;
    $id = preg_replace("/[^0-9]/", '', $id);
    $name = $xpath->query("//div[@id='parameters']/div[contains(.,'linia produktu:')]");
    $name = $name[0]->nodeValue;
    $name = trim(str_replace('linia produktu:', '', $name));
    $group = $xpath->query("//div[@id='parameters']/div[contains(.,'typ produktu:')]");
    $group = $group[0]->nodeValue;
    $group = trim(str_replace('typ produktu:', '', $group));
    $group = preg_replace('/\d+/u', '', $group);
    $group = trim(str_replace('cm', '', $group));
    $lamp = $xpath->query("//div[@id='parameters']/div[contains(.,'ilość trzonków w produkcie:')]");
    $lamp = $lamp[0]->nodeValue;
    $lamp = trim(str_replace('ilość trzonków w produkcie:', '', $lamp));
    $socle = $xpath->query("//div[@id='parameters']/div[contains(.,'trzonek:')]");
    $socle = $socle[0]->nodeValue;
    $socle = trim(str_replace('trzonek:', '', $socle));
    if (empty($socle)){
        $socle = $xpath->query("//div[@id='parameters']/div[contains(.,'rodzaj źródła światła:')]");
        $socle = $socle[0]->nodeValue;
        $socle = trim(str_replace('rodzaj źródła światła:', '', $socle));
        if (strpos($socle, 'LED') !== false) {
            $socle = 'LED';
            }
    }
    $color_stl = $xpath->query("//div[@id='parameters']/div[contains(.,'główny kolor produktu:')]");
    $color_stl = $color_stl[0]->nodeValue;
    $color_stl = trim(str_replace('główny kolor produktu:', '', $color_stl));
    $type_stl = $xpath->query("//div[@id='parameters']/div[contains(.,'główny materiał produktu:')]");
    $type_stl = $type_stl[0]->nodeValue;
    $type_stl = trim(str_replace('główny materiał produktu:', '', $type_stl));

    $size = $xpath->query("//div[@id='parameters']/div[contains(.,'wymiar produktu:')]");
    $size = $size[0]->nodeValue;
    $size = trim(str_replace('wymiar produktu:', '', $size));
    $sizez = explode("x", $size);
    $siz_num = count($sizez)-1;
    $width = preg_replace("/[^0-9]/", '', $sizez[0]);
    $depth = preg_replace("/[^0-9]/", '', $sizez[1]);;
    $height = preg_replace("/[^0-9]/", '', $sizez[$siz_num]);
    if (strpos($size, 'ma') !== false) {
        $depth = $width;
    }

    if (strpos($size, 'mm') !== false){
        $wid_num = strlen($width)-1;
        $dep_num = strlen($depth)-1;
        $hei_num = strlen($height)-1;
        $width = substr($width, 0, $wid_num);
        $depth = substr($depth, 0,$dep_num);
        $height = substr($height, 0,$hei_num);

    }



    $img_o =  $xpath->query("//ul[@class='gallery_big']/li/figure/a");
    foreach ($img_o as $bow){
        $a = $bow->getAttribute('href');
        $pag [] = 'http://www.sanico.com.pl/' . $a;
    }
    if(empty($pag)){
        $img_a =  $xpath->query("//ul[@class='gallery_big']/li/figure/a");
        foreach ($img_a as $bow){
            $b = $bow->getAttribute('href');
            $pag [] = 'http://www.sanico.com.pl/' . $b;
        }
    }
    foreach ($pag as $over){
        $path_to_file = 'C:\Users\игор\Desktop\4wall_4\Polux_sanico\img\\';
        $img  .= 'Polux_sanico_'.basename($over).'|';
        $path = $path_to_file.'Polux_sanico_'.basename($over);
        if(file_exists($path)) { unlink($path); }
        file_put_contents($path, file_get_contents($over));
    }
    $file = 'Polux_sanico.csv';
    $tofile = "$id;$name;$group;;;;$style;$lamp;$socle;$color_lamp;$type_lamp;$color_stl;$type_stl;$width;$height;$depth;$img\n";
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