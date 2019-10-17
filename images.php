

<!DOCTYPE html>
<html>
<title>MHK_Camera</title>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
<style>
* { 
   box-sizing: border-box;
   /*margin works for square screens, no margins for rectangle screen*/
   /*margin-top: 51px;*/
   padding: 0;
}
body {
     font-family: Verdana, sans-serif;
     background: center center no-repeat;
     background-color: black;
     background-size: contain;
    /* height: 50vh;*/
}
.mySlides {display: none;}
img {
vertical-align: middle;
width: 70%;

}

/* Slideshow container */
.slideshow-container {
  max-width: auto;
  max-height: auto;
  position: absolute;
  margin-top: 6vh;
  margin-left: 6vh;
  margin-right: 3vh;
  margin-bottom: 4vh;
  padding-top: 0;
  vertical-align: center;
}

.back {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: visible;
    text-align: center;
    vertical-align: middle;

}

.wraptocenter{
    display: table-cell;
    text-align: center;
    vertical-align: middle;
    width: auto;
    height: auto;
}


/* On smaller screens, decrease text size */
@media only screen and (max-width: 1280px) and (max-height: 1024px) {
  .slideshow-container {margin-top: 15vh;}
}
</style>
</head>
<body>

<body style="overflow:hidden"> 

<?php

//Get a list of file paths using the glob function.
$fileList = glob('images/*.jpg');
//Loop through the array that glob returned.
foreach($fileList as $filename){
   //Simply print them out onto the screen.
	echo "<div class='slideshow-container'>";
	echo "<div class='wraptocenter d-flex justify-content-center'>";
	echo "<div class='mySlides back'> <img src='$filename' style='width:90vw' align='absmiddle'> </div>";
	echo "</div>";
	echo "</div>";
}
?>


<div class="slideshow-container">

<div class="mySlides fade">
  <img src="" style="width:100%">
</div>

<div class="mySlides fade">
  <img src="" style="width:100%">
</div>
<br>


<script>
var slideIndex = 0;
showSlides();
function showSlides() {
  var i;
  //var slideIndex = 0;
  var slides = document.getElementsByClassName("mySlides");
  for (i = 0; i < slides.length; i++) {
	  slides[i].style.display = "none";
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}
  slides[slideIndex-1].style.display = "block";
  if (slideIndex == slides.length-1) {slideIndex = 0}
  if (slideIndex < 48){	 
	  setTimeout(showSlides, 250); // Change image every .25 seconds
  }  
  console.log(slideIndex);
}

setInterval(showSlides,17000);


</script>

</body>
</html>

