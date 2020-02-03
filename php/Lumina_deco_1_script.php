<?php
require("libs\CURL\RollingCurl.class.php");
require("libs\CURL\AngryCurl.class.php");


//чтение url-ов из файла
$file = 'D:\server\OSPanel\domains\parser1.loc\pars_data\data1.txt';
$data = [];
$data = file_get_contents($file);
$urls = explode(" ", $data);
//$urls = unserialize($data);
//echo count($urls);

//foreach ($urls as $ur){
//    echo $ur.'</br>';
//}

//$urls = ['https://centrumswiatla.pl/pl/p/Lumina-Deco-kinkiet-Aurora-LDW-081013-CHR/64567'];

//for ($i = 1; $i <= 5; $i++) {
//
//    $page = 'http://www.aldex.com.pl/kuchenne?page='. $i;
//    $urls []= $page;
//}

$file2 = 'D:\server\OSPanel\domains\parser1.loc\pars_data\data2.txt';
function request_callback1($response, $info)
{
    global $pages;
    $img='';
    $style ='';
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

    $doc = new DOMDocument;
    $doc->preserveWhiteSpace = false;
    @$doc->loadHTML($response);
    $xpath = new DOMXPath($doc);

    $id = $xpath->query("//div[@class='row code']/em[contains(text(),'Kod producenta:')]/following::span[1]");
    $id = $id[0]->nodeValue;
    $id = trim($id);
    $upsok = $xpath->query("//h1");
    $upsok = $upsok[0]->nodeValue;
    if (strpos($upsok, 'Lampa podłogowa') !== false) {
        $group = 'Lampa podłogowa';
    }
    if (strpos($upsok, 'lampa podłogowa') !== false) {
        $group = 'Lampa podłogowa';
    }
    if (strpos($upsok, 'lampa wisząca') !== false) {
        $group = 'lampa wisząca';
    }
    if (strpos($upsok, 'lampy wiszące') !== false) {
        $group = 'lampa wisząca';
    }
    if (strpos($upsok, 'lampa wiszaca') !== false) {
        $group = 'lampa wisząca';
    }
    if (strpos($upsok, 'plafon') !== false) {
        $group = 'plafon';
    }
    if (strpos($upsok, 'lampa stojąca') !== false) {
        $group = 'lampa stojąca';
    }
    if (strpos($upsok, 'kinkiet') !== false) {
        $group = 'kinkiet';
    }
    if (strpos($upsok, 'lampy biurkowe') !== false) {
        $group = 'lampy biurkowe';
    }
    if (strpos($upsok, 'lampka biurkowa') !== false) {
        $group = 'lampy biurkowe';
    }
    if (strpos($upsok, 'lampy stołowe') !== false) {
        $group = 'lampy stołowe';
    }
    $flap = $xpath->query("//div[@class='resetcss']/p");
    $flap = $flap[0]->nodeValue;
    $flip = explode(":", $flap);
    $flop = count($flip) -1;
    for ($i = 1; $i <= $flop; $i++) {
        $chap = $xpath->query('//div[@class="resetcss"]/p/text()['.$i.']');
        $chap = $chap[0]->nodeValue;

        if (strpos($chap, 'Gwint/Trzonek:') !== false) {
            $socle = trim(str_replace('Gwint/Trzonek:', '', $chap));
        }
        if (strpos($chap, 'Ilość punktów światła:') !== false) {
            $lamp = trim(str_replace('Ilość punktów światła:', '', $chap));
        }
        if (strpos($chap, 'Kolor:') !== false) {
            $color_stl = trim(str_replace('Kolor:', '', $chap));
        }
        if (strpos($chap, 'Materiał lampy:') !== false) {
            $type_stl = trim(str_replace('Materiał lampy:', '', $chap));
        }
        if (strpos($chap, 'Styl:') !== false) {
            $style = trim(str_replace('Styl:', '', $chap));
        }
        if (strpos($chap, 'Szerokość lampy:') !== false) {
            $width = preg_replace("/[^0-9]/", '', $chap);
        }
        if (strpos($chap, 'Wysokość lampy:') !== false) {
            $height = preg_replace("/[^0-9]/", '', $chap);
        }
        if (strpos($chap, 'Średnica lampy:') !== false) {
            $depth = preg_replace("/[^0-9]/", '', $chap);
        }
    }


    $img_o =  $xpath->query("//div[@class='innersmallgallery']/ul/li/a");
    foreach ($img_o as $bow){
        $a = $bow->getAttribute('href');
        $pag [] = 'https://centrumswiatla.pl' . $a;
    }
    if (count($pag) == 0){
        $img_a =  $xpath->query("//div[@class='mainimg productdetailsimgsize row']/a");
        foreach ($img_a as $bow){
            $a = $bow->getAttribute('href');
            $pag [] = 'https://centrumswiatla.pl' . $a;
        }
    }
    foreach ($pag as $over){
        $path_to_file = 'C:\Users\игор\Desktop\4wall_4\Lumina_Deco\img\\';
        $img  .= 'Lumina_Deco_'.basename($over).'|';
        $path = $path_to_file.'Lumina_Deco_'.basename($over);
        if(file_exists($path)) { unlink($path); }
        file_put_contents($path, file_get_contents($over));
    }
    $file = 'Lumina_Deco.csv';
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