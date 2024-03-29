/*------------------------------------------------Сделаем блоки белыми - после "детали"----------------------------------------------------------------------*/

$('.vacancies, .payment, .age, .rubric, .city_link, .views_count, .published').wrapAll('<div class="adaptive_white">');
$('.phone_num_span, .phone_number, .email_span').wrapAll('<div class="adaptive_white">');
/*------------------------------------------------ФОТОГРАФИИ----------------------------------------------------------------------*/
var photos_number = 3;
const img1_src = document.getElementById('img1').getAttribute("src");
if(!img1_src){
	document.getElementById('label1').style.display = "none";
	document.getElementById('slide1').style.display = "none";
	photos_number--;
}
const img2_src = document.getElementById('img2').getAttribute("src");
if(!img2_src){
	document.getElementById('label2').style.display = "none";
	document.getElementById('slide2').style.display = "none";
	photos_number--;
}
const img3_src = document.getElementById('img3').getAttribute("src");
if(!img3_src){
	document.getElementById('label3').style.display = "none";
	document.getElementById('slide3').style.display = "none";
	document.getElementById('navigation_manual').style.width = "120px";
	photos_number--;
}

if(photos_number === 1){
	document.getElementById('navigation_manual').style.display = "none";
	document.getElementById('arr_bck').style.display = "none";
	document.getElementById('arr_frwrd').style.display = "none";
}

var counter = 1;
const arrow_back = document.getElementById('arr_bck');
const arrow_forward = document.getElementById('arr_frwrd');

const radio1 = document.getElementById('radio1');
const radio2 = document.getElementById('radio2');
const radio3 = document.getElementById('radio3');

const label1 = document.getElementById('label1');
const label2 = document.getElementById('label2');
const label3 = document.getElementById('label3');
check_radio1();
function check_radio1(){
	radio1.checked = true;
	label1.style.background = "rgba(0, 0, 0, 0.5)";
	label2.style.background = "transparent";
	label3.style.background = "transparent";
    counter = 1;
}
function check_radio2(){
	label1.style.background = "transparent";
	label2.style.background = "rgba(0, 0, 0, 0.5)";
	label3.style.background = "transparent";
    counter = 2;
}
function check_radio3(){
	label1.style.background = "transparent";
	label2.style.background = "transparent";
	label3.style.background = "rgba(0, 0, 0, 0.5)";
    counter = 3;
}

arrow_forward.onclick = function(e) { 
	counter++;
	if (counter > photos_number){counter = 1;}
	document.getElementById('radio' + counter).checked = true;
	document.getElementById('label' + counter).style.background = "rgba(0, 0, 0, 0.5)";
	if(counter > 1){
		document.getElementById('label' + (counter-1)).style.background = "transparent";
	}
	else{
		document.getElementById('label' + (photos_number)).style.background = "transparent";
	}
};
arrow_back.onclick = function(e) { 
	counter--;
	if (counter < 1){counter = photos_number;}
	document.getElementById('radio' + counter).checked = true;
	document.getElementById('label' + counter).style.background = "rgba(0, 0, 0, 0.5)";
	if(counter < photos_number){
		document.getElementById('label' + (counter+1)).style.background = "transparent";
	}
	else{
		document.getElementById('label1').style.background = "transparent";
	}
};




if (document.getElementsByClassName('phone_number')) {
	document.getElementsByClassName('phone_number')[0].onclick = function(){
		var textArea = document.createElement("textarea");
		textArea.value = document.getElementsByClassName('phone_number')[0].innerText;
		document.body.appendChild(textArea);
		textArea.select();
		document.execCommand("Copy");
		textArea.remove();
		help_copied_phone_show();
	}
}

function help_copied_phone_show(){
    document.querySelector('.help_copied_phone').style.visibility='visible';
    document.querySelector('.help_copied_phone').style.opacity='1';
    setTimeout(help_copied_phone_hide, 1800);
}
function help_copied_phone_hide(){
document.querySelector('.help_copied_phone').style.opacity='0';
setTimeout(help_copied_phone_block_hide, 600);
}
function help_copied_phone_block_hide(){
document.querySelector('.help_copied_phone').style.visibility='hidden';
}

/*---------------------------------- СВАЙП ФОТОГРАФИЙ ПРИ АДАПТИВЕ -----------------------------------------------------*/
var elements = document.getElementsByClassName("slide");
Array.from(elements).forEach(function(element) {
	element.addEventListener('touchstart', handleTouchStart, false);        
	element.addEventListener('touchmove', handleTouchMove, false);
	element.addEventListener('touchend', handleTouchEnd, false);
});


var xDown = null;                                                        
var yDown = null;

var touchmoved = false;

function getTouches(evt) {
  return evt.touches ||             // browser API
         evt.originalEvent.touches; // jQuery
}                                                     
                                                                         
function handleTouchStart(evt) {
    const firstTouch = getTouches(evt)[0];                                      
    xDown = firstTouch.clientX;                                      
    yDown = firstTouch.clientY;	
};  

function handleTouchEnd(evt){
	if(touchmoved != true){
		// not moved then clicked
		openPhoto();
	}
	
	$('.photo_slides').on('touchmove', function(e){
		touchmoved = true;
	}).on('touchstart', function(){
		touchmoved = false;
	});
}
                                                                         
function handleTouchMove(evt) {
    if ( ! xDown || ! yDown ) {
        return;
    }

	var xUp = evt.touches[0].clientX;                                    
	var yUp = evt.touches[0].clientY;

	var xDiff = xDown - xUp;
	var yDiff = yDown - yUp;
																			
	if ( Math.abs( xDiff ) > Math.abs( yDiff ) ) {/*most significant*/
		if ( xDiff > 0 ) {
			/* right swipe */ 
			arrow_forward.click();
		}
		else {
			/* left swipe */
			arrow_back.click();
		}     
							
	} 
	// else {
	//     if ( yDiff > 0 ) {
	//         /* down swipe */ 
	//     } else { 
	//         /* up swipe */
	//     }                                                                 
	// }
	/* reset values */
	xDown = null;
	yDown = null;  
                                           
};


/*---------------------------------- Вставим блоки "Детали" при адаптиве ------------------------------------------------------------*/

if(window.location.href.includes('/uk/')){
	// $( ".title" ).after( "<span class='heading_span'>Деталі:</span>" );
	// $( ".employer" ).after( "<span class='heading_span_emp'>Контакти:</span>" );
	// $( ".description" ).before( "<span class='description_header'>Опис:</span>" );
}
else{
	// $( ".title" ).after( "<span class='heading_span'>Детали:</span>" );
	// $( ".employer" ).after( "<span class='heading_span_emp'>Контакты:</span>" );
	// $( ".description" ).before( "<span class='description_header'>Описание:</span>" );
	$( ".title" ).after( "<span class='heading_span'>Деталі:</span>" );
	$( ".employer" ).after( "<span class='heading_span_emp'>Контакти:</span>" );
	$( ".description" ).before( "<span class='description_header'>Опис:</span>" );
}
/*---------------------------------- Проверяем кол-во слов в нашем описании ------------------------------------------------------------*/

// Если у нас info не fixed, значит, мы не на главной
const info = document.querySelector('.info');
if(document.querySelector('.description').textContent.split(' ').length > 50 && getComputedStyle(info).position !== 'fixed'){
	if(window.location.href.includes('/uk/')){
		// $( ".description" ).after( "<span class='description_more'>Показати більше</span>" );
	}
	else{
		$( ".description" ).after( "<span class='description_more'>Показати більше</span>" );
	}

	document.querySelector('.description').style.height = '100px';
	document.querySelector('.description').style.overflow = 'hidden';
	// делаем лёгкое затемнение текста под конец описания
	document.querySelector('.description').style.setProperty("--description-background", "rgba(255, 255, 255, 0.8)");


	document.querySelector('.description_more').onclick = function() {
			document.querySelector('.description').style.height = 'auto';
			document.querySelector('.description_more').style.display = 'none';

			window.scrollTo({
					top: 1000,
					behavior: 'smooth',});
			
			document.querySelector('.description').style.setProperty("--description-background", "none");
	}

}
/*-------------------------- ЕСЛИ ПОЛЬЗОВАТЕЛЬ 24Ч, ТО ОТКРЫВАЕМ BOTTOM NAV ---------------------------------------------------------*/
// Если у нас info не fixed, значит, мы не на главной     Если у нас поле отправки сообщения нету, тогда этот пользователь - мы сами
if(document.querySelector('.h24') || !document.querySelector('.send_message_field') && getComputedStyle(info).position !== 'fixed'){
	const bottom_navigation = document.querySelector('.bottom_navigation');
	var emp = document.querySelector(".emp");
	var cookies_mob = document.querySelector('.accept_cookie');
	bottom_navigation.style.display = 'block'
	window.addEventListener('scroll', ()=>{
		let scrolled = window.scrollY;
		arr.push(scrolled);
  
		for(let i=arr.length-1; i<=arr.length; i++){
			if(arr[i-1] > arr[i]){
			  bottom_navigation.classList.remove("bot_nav_hide");
			  cookies_mob.style.bottom = '50px';
			  emp.classList.remove("emp_hide");
			}
			if(arr[i-1] < arr[i]){
			  bottom_navigation.classList.add("bot_nav_hide");
			  cookies_mob.style.bottom = '0';
			  emp.classList.add("emp_hide");
			}        
		}
	})
}


/*---------------------------------- ДВИГАЕМ НИЖНЮЮ ПОЛОСУ ОТПРАВКИ СООБЩЕНИЯ и PAGE_TITLE-------------------------------------------------------*/
var send_message_field = document.querySelector(".send_message_field");
var arr = [0];

window.addEventListener('scroll', ()=>{
  let scrolled = window.scrollY;
  arr.push(scrolled);
  var emp = document.querySelector(".emp");

  for(let i=arr.length-1; i<=arr.length; i++){
      if(arr[i-1] > arr[i]){
		if (send_message_field){
        	send_message_field.classList.remove("smf_hide");
		}
		cookies_mob.style.bottom = '50px';
        emp.classList.remove("emp_hide");
      }
      if(arr[i-1] < arr[i]){
		if (send_message_field){
        	send_message_field.classList.add("smf_hide");
		}
		cookies_mob.style.bottom = '0';
        emp.classList.add("emp_hide");
      }        
  }
})
$( ".description" ).after( "<span class='close_img'>+</span>" );
/*---------------------------------- Открываем фото на весь экран -------------------------------------------------------*/
var close_img = document.querySelector('.close_img');
if(close_img){
	close_img.onclick = function(e) { openPhoto();}
}

function openPhoto(){
	var photo_slides = document.querySelector('.photo_slides');
	var slider = document.querySelector('.slider');
	var slides = document.querySelector('.slides');
	var slide = document.querySelectorAll('.slide');
	var img1 = document.getElementById('img1');
	var img2 = document.getElementById('img2');
	var img3 = document.getElementById('img3');
	if(document.querySelector('.photo_slides').style.background === 'rgb(0, 0, 0)'){
		close_img.style.display = null;

		photo_slides.style.margin = null;
		photo_slides.style.width = null;
		photo_slides.style.position = null;
		photo_slides.style.zIndex = null;
		photo_slides.style.background = null;
		photo_slides.style.height = null;
		photo_slides.style.display = null;
		photo_slides.style.alignItems = null;

		slider.style.overflow = null;
		slider.style.height = null;

		slides.style.display = null;

		slide.forEach(function(el) {
			el.style.zIndex = null;
			el.style.display = null;
			el.style.alignItems = null;
		});

		img1.style.maxHeight = null;	
		img2.style.maxHeight = null;	
		img3.style.maxHeight = null;
	}
	else{
		close_img.style.display = 'inline-block';

		photo_slides.style.margin = '0';
		photo_slides.style.width = '100%';
		photo_slides.style.position = 'fixed';
		photo_slides.style.zIndex = '1001';
		photo_slides.style.background = '#000';
		photo_slides.style.height = '100%';
		photo_slides.style.display = 'flex';
		photo_slides.style.alignItems = 'center';

		slider.style.overflow = 'visible';
		slider.style.height = '100%';

		slides.style.display = 'flex';

		slide.forEach(function(el) {
			el.style.zIndex = '1';
			el.style.display = 'flex';
			el.style.alignItems = 'center';
		});

		img1.style.maxHeight = '100%';	
		img2.style.maxHeight = '100%';	
		img3.style.maxHeight = '100%';
	}
}


window.addEventListener("orientationchange", function(event) {
	var photo_slides = document.querySelector('.photo_slides');
	var slide = document.querySelectorAll('.slide');

	if(document.querySelector('.photo_slides').style.background === 'rgb(0, 0, 0)'){
		// Portrait
		if(screen.availHeight > screen.availWidth){
			slide.forEach(function(el) {
				el.style.zIndex = '1';
				el.style.display = 'flex';
				el.style.alignItems = 'center';
				el.style.justifyContent = null;
			});
		}
		// Landscape
		else{
			slide.forEach(function(el) {
				el.style.zIndex = '1';
				el.style.display = 'flex';
				el.style.justifyContent = 'center';
				el.style.alignItems = null;
			});
		}
	}
	else{
		slide.forEach(function(el) {
			el.style.zIndex = null;
			el.style.display = null;
			el.style.alignItems = null;
		});
	}
});