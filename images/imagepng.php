<?php
//function create_image()
//{
	$imagecontainer = imagecreatetruecolor(500,550);
	imagesavealpha($imagecontainer, true);

	$alphacolor = imagecolorallocatealpha($imagecontainer, 0,0,0,127);
	imagefill($imagecontainer,0,0,$alphacolor);

	$background = imagecreatefrompng('background.png');
	// Copy the background into the container
	imagecopyresampled($imagecontainer, $background, 0, 0, 0, 0, 500, 550, 500, 550);

	$order = $_GET['order'];
	$kid = $_GET['kID'];
	$age = $_GET['age'];
	$name = $_GET['name'];
	$kidinfo = $name . ', ' . $age;
	$artscience = $_GET['artscience'];
	$game = $_GET['game'];
	$experience = $_GET['experience'];
	$interest = $_GET['interest'];
	$estimation = $_GET['estimation'];
	$group = $_GET['group'];
	$font = './Quicksand-Bold.ttf';
	$foreground = imagecolorallocate($imagecontainer, 255,255,255); 
	imagettftext($imagecontainer, 30, 0, 22, 44, $foreground, $font, $order); 
	imagettftext($imagecontainer, 35, 0, 135, 84, $foreground, $font, 'KIDO'.$kid); 
	imagettftext($imagecontainer, 18, 0, 60, 152, $foreground, $font, $kidinfo); 
	imagettftext($imagecontainer, 22, 0, 329, 195, $foreground, $font, $artscience); 
	imagettftext($imagecontainer, 22, 0, 329, 248, $foreground, $font, $game); 
	imagettftext($imagecontainer, 22, 0, 329, 300, $foreground, $font, $experience); 
	imagettftext($imagecontainer, 22, 0, 329, 352, $foreground, $font, $interest);
	imagettftext($imagecontainer, 22, 0, 329, 404, $foreground, $font, $estimation);
	imagettftext($imagecontainer, 22, 0, 329, 457, $foreground, $font, $group);
	
	$avatar = imagecreatefrompng('avatar.png');
	imagecopyresampled($imagecontainer, $avatar, 53, 181, 0, 0, 145, 185, 145, 185);
	
	$gender = $_GET['gender'];
	if ($gender == 2) { $genderImage = imagecreatefrompng('female.png'); } 
	else { $genderImage = imagecreatefrompng('male.png'); }
	imagecopyresampled($imagecontainer, $genderImage, 35, 136, 0, 0, 16, 16, 16, 16);
	
	$r = $_GET['r'];
	if ($r == 1) { $rImage = imagecreatefrompng('bad.png'); }
	else if ($r == 2) {  $rImage = imagecreatefrompng('average.png'); }
	else { $rImage = imagecreatefrompng('good.png'); }
	imagecopyresampled($imagecontainer, $rImage, 138, 432, 0, 0, 27, 27, 27, 27);
	
	$c = $_GET['c'];
	if ($c == 1) { $cImage = imagecreatefrompng('bad.png'); }
	else if ($c == 2) {  $cImage = imagecreatefrompng('average.png'); }
	else { $cImage = imagecreatefrompng('good.png'); }
	imagecopyresampled($imagecontainer, $cImage, 88, 432, 0, 0, 27, 27, 27, 27);
	
	$e = $_GET['e'];
	if ($e == 1) { $eImage = imagecreatefrompng('bad.png'); }
	else if ($e == 2) {  $eImage = imagecreatefrompng('average.png'); }
	else { $eImage = imagecreatefrompng('good.png'); }
	imagecopyresampled($imagecontainer, $eImage, 188, 432, 0, 0, 27, 27, 27, 27);
	
	$t = $_GET['t'];
	if ($t == 1) { $tImage = imagecreatefrompng('bad.png'); }
	else if ($t == 2) {  $tImage = imagecreatefrompng('average.png'); }
	else { $tImage = imagecreatefrompng('good.png'); }
	imagecopyresampled($imagecontainer, $tImage, 38, 432, 0, 0, 27, 27, 27, 27);
	//header('Content-Disposition: Attachment;filename=KIDO'.$kid.'.png');
	//try to get the image
	header("Content-Type: image/png");
	// Finally render the container
	imagepng($imagecontainer, './kids/KIDO'.$kid.'.png');
	imagedestroy($imagecontainer);
//}
//echo '<img src="'.create_image().'"/>';
?>
