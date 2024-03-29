/*------------------------------------------------ COOKIES----------------------------------------------------------------------*/
/*----------- МЕНЯЕМ ЛОГОТИП, ЕСЛИ ТЁМНАЯ ТЕМА ---------------------*/
if(document.querySelector('.logo_teenwork')){
  if(getCookie('theme') === 'dark'){
    $(".logo_teenwork_img").attr("src","/static/img/white_logo.svg");
  }
  else{
    $(".logo_teenwork_img").attr("src","/static/img/logo.svg");
  }
}

var main = document.querySelector('.main');
var toggle = document.querySelector('.toggle');
if (toggle !== null) {
  toggle.onclick = function(){
    if(getCookie('theme') === 'dark'){
      document.cookie = "theme=light; path=/; max-age=2592000; samesite=lax";
      main.classList.remove('dark');

      $("html").removeClass("dark_scroll"); // СМЕНА ЦВЕТА ПОЛОСЫ ПРОКРУТКИ
      $("body").removeClass("dark_scroll");
      
      $(".logo_teenwork_img").attr("src","/static/img/logo.svg"); // логотип
    }
    else if(getCookie('theme') === 'light'){
      document.cookie = "theme=dark; path=/; max-age=2592000; samesite=lax";
      main.classList.add('dark');

      $("html").addClass("dark_scroll");
      $("body").addClass("dark_scroll");

      $(".logo_teenwork_img").attr("src","/static/img/white_logo.svg"); // логотип
    }
    else{
      document.cookie = "theme=dark; path=/; max-age=2592000; samesite=lax";
      main.classList.add('dark');

      $("html").addClass("dark_scroll");
      $("body").addClass("dark_scroll");
    }
  }
}
if(getCookie('theme') === 'dark'){
  main.classList.add('dark');
  $("html").addClass("dark_scroll");
  $("body").addClass("dark_scroll");
}
else if(getCookie('theme') === 'light'){
  main.classList.remove('dark');
  $("html").removeClass("dark_scroll");
  $("body").removeClass("dark_scroll");
}
/*------------------------------------------------ LANGUAGE COOKIE----------------------------------------------------------------------*/
const lang_checkbox = document.getElementById('lang_checkbox');
const lang_checkbox_others = document.getElementById('lang_checkbox_others');
var url = window.location.href;
if(lang_checkbox){
lang_checkbox.onchange = function() {
  if (lang_checkbox.checked) {
    document.location.href = '/en/'
    if(url.includes('/others_page/')){
      if(getCookie('theme') === 'dark'){
        document.getElementsByClassName('en')[0].style.color = '#fff';
        document.getElementsByClassName('en')[1].style.color = '#fff';
      }
    }
  }
  else{
    document.location.href = '/'
    if(url.includes('/others_page/')){
      if(getCookie('theme') === 'dark'){
        document.getElementsByClassName('uk')[0].style.color = '#fff';
        document.getElementsByClassName('uk')[1].style.color = '#fff';
      }
    }
  }

  if(getCookie('lang') === 'en'){
    document.cookie = "lang=uk; path=/; max-age=2592000; samesite=lax";
    
    if(url.includes('/others_page/')){
      if(getCookie('theme') === 'dark'){
        document.getElementsByClassName('en')[0].style.color = '#fff';
        document.getElementsByClassName('en')[1].style.color = '#fff';
      }
    }
  }
  else if(getCookie('lang') === 'uk'){
    document.cookie = "lang=en; path=/; max-age=2592000; samesite=lax";
    
    if(url.includes('/others_page/')){
      if(getCookie('theme') === 'dark'){
        document.getElementsByClassName('uk')[0].style.color = '#fff';
        document.getElementsByClassName('uk')[1].style.color = '#fff';
      }
    }
  }
  else{
    document.cookie = "lang=uk; path=/; max-age=2592000; samesite=lax";
    
    if(url.includes('/others_page/')){
      if(getCookie('theme') === 'dark'){
        document.getElementsByClassName('uk')[0].style.color = '#fff';
        document.getElementsByClassName('uk')[1].style.color = '#fff';
      }
    }
  }
}
}

if(getCookie('lang') === 'en'){
  if(lang_checkbox){
    lang_checkbox.checked = true;
  }
  if(lang_checkbox_others){
    lang_checkbox_others.checked = true;
  }

  if(document.querySelector('.uk')){
    document.getElementsByClassName('en')[0].style.color = '#000';
    document.getElementsByClassName('uk')[0].style.color = '#c6c6c6';
  }


  if(url.includes('/others_page/')){
    if(getCookie('theme') === 'dark'){
      document.getElementsByClassName('uk')[0].style.color = '#fff';
      document.getElementsByClassName('uk')[1].style.color = '#fff';
    }
  }
}
else if(getCookie('lang') === 'uk'){
  if(lang_checkbox){
    lang_checkbox.checked = false;
  }
  if(lang_checkbox_others){
    lang_checkbox_others.checked = false;
  }
  if(document.querySelector('.en')){
    document.getElementsByClassName('uk')[0].style.color = '#000';
    document.getElementsByClassName('en')[0].style.color = '#c6c6c6';
  }

  if(url.includes('/others_page/')){
    if(getCookie('theme') === 'dark'){
      document.getElementsByClassName('en')[0].style.color = '#fff';
      document.getElementsByClassName('en')[1].style.color = '#fff';
    }
  }
}



if(url.includes('/en/')){
  if(lang_checkbox){
    lang_checkbox.checked = true;
  }
  document.cookie = "lang=uk; path=/; max-age=2592000; samesite=lax";

  if(document.querySelector('.en')){
    document.getElementsByClassName('en')[0].style.color = '#000';
    document.getElementsByClassName('uk')[0].style.color = '#c6c6c6';
  }

  if(url.includes('/others_page/')){
    document.getElementsByClassName('en')[1].style.color = '#000';
    document.getElementsByClassName('uk')[1].style.color = '#c6c6c6';
  }
}
else{
  if(lang_checkbox){
    lang_checkbox.checked = false;
  }
  document.cookie = "lang=en; path=/; max-age=2592000; samesite=lax";
  if(document.querySelector('.en')){
    document.getElementsByClassName('uk')[0].style.color = '#000';
    document.getElementsByClassName('en')[0].style.color = '#c6c6c6';
  }
  if(url.includes('/others_page/')){
    document.getElementsByClassName('uk')[1].style.color = '#000';
    document.getElementsByClassName('en')[1].style.color = '#c6c6c6';
  }
}
// Others page checkbox click
if(lang_checkbox_others){
  lang_checkbox_others.onchange = function() {
    if(lang_checkbox_others.checked === true){
      lang_checkbox.click();
    }
    else{
      lang_checkbox.click();
    }
  }
}
////////////////////////////////////////////// СМЕНА ЦВЕТА HEADER ГРАДИЕНТ ///////////////////////////////////////
var test = document.querySelector(".test");
var now = new Date();
if(test){
if (now.getHours() === 0 || now.getHours() === 1 || now.getHours() === 2 || now.getHours() === 3 || now.getHours() === 4 || now.getHours() === 5){
  test.style.backgroundImage = '';
  test.style.background = '#1e2b55';
}
else if(now.getHours() === 6 || now.getHours() === 7 || now.getHours() === 8 || now.getHours() === 9 || now.getHours() === 10 || now.getHours() === 11){
  test.style.background = '';
  test.style.backgroundImage = 'linear-gradient(to right, #7c6997, #ba759c, #ea898f, #ffac7c, #f9d978)';
}
else if(now.getHours() === 12 || now.getHours() === 13 || now.getHours() === 14 || now.getHours() === 15 || now.getHours() === 16 || now.getHours() === 17){
  test.style.background = '';
  test.style.backgroundImage = 'linear-gradient(to right, #f9d978, #faca6d, #faba64, #faab5e, #f89b5a)';
}
else if(now.getHours() === 18 || now.getHours() === 19 || now.getHours() === 20){
  test.style.background = '';
  test.style.backgroundImage = 'linear-gradient(to right, #f89b5a, #f4757a, #ce639d, #8862b1, #0062a9)';
}
else if(now.getHours() === 21 || now.getHours() === 22 || now.getHours() === 23){
  test.style.background = '';
  test.style.backgroundImage = 'linear-gradient(to right, #0062a9, #195393, #1f457e, #203869, #1e2b55)';
}
}
//------------------------------------------------------------------------COOKIES FIELD

var accept_cookie = document.querySelector('.accept_cookie');
var cookie_submit_button = document.querySelector('.cookie_submit_button');
var add_nav = document.querySelector('.add_nav');
if (cookie_submit_button !== null) {
  cookie_submit_button.onclick = function(){
    document.cookie = "cookies_accept=true; path=/; max-age=31536000; samesite=lax";
    accept_cookie.classList.remove('cookies_show');

    try_24h.classList.add('try_24h_show');

    if (window.innerWidth < 1367){
      add_nav.style.animation = 'none';
    }
  }
}
if(add_nav){
if(getCookie('cookies_accept') === 'true'){
  accept_cookie.classList.remove('cookies_show');
  if (window.innerWidth < 1367){
    add_nav.style.animation = 'none';
  }
}
else{
  accept_cookie.classList.add('cookies_show');
  if (window.innerWidth < 1367){
    add_nav.style.animation = 'pulse 0.4s alternate infinite';
  }
}
}
//------------------------------------------------------------------------- 24 HOUR FIELD
var try_24h = document.querySelector('.try_24h');
var try_24h_submit_button = document.querySelector('.try_24h_submit_button');
if (try_24h_submit_button !== null) {
  try_24h_submit_button.onclick = function(){
    document.cookie = "try_24h=true; path=/; max-age=31536000; samesite=lax";
    try_24h.classList.remove('try_24h_show');
  }
}
if(getCookie('try_24h') === 'true'){
  if(try_24h){
    try_24h.classList.remove('try_24h_show');
  }
}
if(getCookie('try_24h') === undefined && getCookie('cookies_accept') === 'true'){
  if(try_24h){
    try_24h.classList.add('try_24h_show');
  }
}


function getCookie(name) {
  var matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

