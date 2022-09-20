/*----------------------------------------ДОБАВЛЕНИЕ НЕСКОЛЬКИХ ФОТО И ИХ ОТОБРАЖЕНИЕ -------------------------------------------------*/
var photo1_img_uploaded = false;
$(document).ready(function() {
  $('input[name=img]').change(function(e) {
      document.querySelector('.upload_button').classList.add('button_loading');
      e.preventDefault(); 
      var data = new FormData($('#ajax')[0]);

      $.ajax({
          url: '/add/',
          type: 'POST',
          data: data,
          processData: false,
          contentType: false,
          success: function(data) {
              // data = JSON.parse(data); // converts string of json to object
              $('#photo1').html('<img src="' + data.url1 + '" onError="this.style.display=\'none\'" style="object_fit: cover; width:100%; height:100%;" id="photo1_img"/>');
              $('#photo2').html('<img src="' + data.url2 + '" onError="this.style.display=\'none\'" style="object_fit: cover; width:100%; height:100%;" id="photo2_img"/>');
              $('#photo3').html('<img src="' + data.url3 + '" onError="this.style.display=\'none\'" style="object_fit: cover; width:100%; height:100%;" id="photo3_img"/>');
              document.querySelector('.upload_button').classList.remove('button_loading'); // добавляем крутилку на кнопку добавления фотографий
              help_image_text_show();

              $("#photo1_src").attr("value", $("#photo1_img").attr('src'));
              $("#photo2_src").attr("value", $("#photo2_img").attr('src'));
              $("#photo3_src").attr("value", $("#photo3_img").attr('src'));

              // Проверка, если есть изображение, отключаем эффекты
              photo1.style.boxShadow = "0 0 4px rgba(0, 0, 0, 0.3)";
              upload_button.style.animation = "none";

              photo1_img_uploaded = true;
            }
      });
      return false;
  });

  if (window.location.href.indexOf("add") > -1) { // Если мы находимся на странице добавления, а не изменения
    $("#boardForm").on('submit', (function(e) {
      /* Переменные, которые передают значения ном.тел и email для проверки 24ч объявления */
      var phone_num = document.getElementById("id_phone_number").value;
      var email = document.getElementById("id_email").value;

      $("#photo1_pos").attr("value", $('#cloned_photos #photo1').attr("data-pos"));
      $("#photo2_pos").attr("value", $('#cloned_photos #photo2').attr("data-pos"));
      $("#photo3_pos").attr("value", $('#cloned_photos #photo3').attr("data-pos"));

      $.ajax({
        url: '/add/',
        type: 'POST',
        async: false,
        data: {
          'phone_num':phone_num,
          'email':email,
        },
        success: function(data) {
          if(data === 'less_than_3'){
            //console.log(data)
          }
          else if(data === 'more_than_3'){
            e.preventDefault();
            alert('Пожалуйста, чтобы добавить больше записей, создайте аккаунт');
          }
          else{
            e.preventDefault();
            alert('Попробуйте ещё раз');
          }
        },
        error: function(){
          e.preventDefault();
          alert('Попробуйте ещё раз!');
        }
      });
    }));
  }
});

/*----------------------------------------------- Автозаполнение ПОЛЕЙ С ДАННЫМИ ПОЛЬЗОВАТЕЛЯ -------------------------------------------------------------*/
$(document).ready(function(){              
  $.ajax({
    url: '/add/',
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    type: 'POST',
    data: {
      'user_data': 'user_data',
    },
    success: function(data) {
      var first_name = data[0];
      var last_name = data[1];
      var phone = data[2];
      var em = data[3];
      if(first_name !== null){ // Если пользователь зарегестрирован. У незарегестрированного undefined
        if(first_name !== '' || last_name !== ''){
          document.getElementById('id_author_name').value = first_name + ' ' + last_name;
        }
        document.getElementById('id_phone_number').value = phone;
        document.getElementById('id_email').value = em;
      }
    },
  });
});

/*-----------------------------------------------ПРОВЕРКА ВВЕДЁННОЙ ЗАРПЛАТЫ-------------------------------------------------------------*/
function getSal() {
    const val = document.querySelector('.adt_salary').value;
    if (val >=0){
        document.querySelector('.adt_salary').style.borderBottom  = "0.2px solid rgba(0, 0, 0, 0)";
    }
    else if (val < 0){
        document.querySelector('.adt_salary').value = 0;
        document.querySelector('.adt_salary').style.borderBottom  = "0.2px solid rgba(0, 0, 0, 0)";
    }
}
/*--------------------------------------------РЕГИОН И ГОРОД----------------------------------------------------------------*/
$("#id_region").change(function () {
    var url = $("#boardForm").attr("data-branches-url");  
    var regionId = $(this).val();  

    $.ajax({                      
      url: url,                    
      data: {
        'region': regionId
      },
      success: function (data) {  
        $("#id_city").html(data);  
      }
    });

  });
/*--------------------------------------ПОКАЗЫВАЕМ ВСПОМОГАТЕЛЬНОЕ ОКНО ПОСЛЕ ЗАГРУЗКИ ИЗОБРАЖЕНИЙ----------------------------------------------------------------------*/
function help_image_text_show(){
  document.querySelector('.help_image_text').style.display='block';
  document.querySelector('.help_image_text').style.opacity='1';
  document.querySelector('.help_image_text').style.visibility='visible';
  setTimeout(help_image_text_hide, 3000);
}
function help_image_text_hide(){
  document.querySelector('.help_image_text').style.visibility='hidden';
  document.querySelector('.help_image_text').style.opacity='0';
  setTimeout(help_image_text_block_hide, 600);
}
function help_image_text_block_hide(){
  document.querySelector('.help_image_text').style.display='none';
}
/*-------------------------------------------ПЕРЕТАСКИВАНИЕ ИЗОБРАЖЕНИЙ-----------------------------------------------------------------*/
$(".photo").each(function (i) {
    var item = $(this);
    i=i-1
    var item_clone = item.clone();
    item.data("clone", item_clone);
    var position = item.position();
    item_clone
      .css({
        left: position.left,
        top: position.top,
        visibility: "hidden"
      })
      .attr("data-pos", i + 1);
  
    $("#cloned_photos").append(item_clone);
  });
  
  $(".photos").sortable({
    axis: "x",
    revert: true,
    scroll: false,
    placeholder: "sortable-placeholder",
    cursor: "move",
  
    start: function (e, ui) {
      ui.helper.addClass("exclude-me");
      $(".photos .photo:not(.exclude-me)").css("visibility", "hidden");
      ui.helper.data("clone").hide();
      $(".cloned_photos .photo").css("visibility", "visible");
    },
  
    stop: function (e, ui) {
      $(".photos .photo.exclude-me").each(function () {
        var item = $(this);
        var clone = item.data("clone");
        var position = item.position();
  
        clone.css("left", position.left);
        clone.css("top", position.top);
        clone.show();
  
        item.removeClass("exclude-me");
      });
  
      $(".photos .photo").each(function () {
        var item = $(this);
        var clone = item.data("clone");
  
        clone.attr("data-pos", item.index());
      });
  
      $(".photos .photo").css("visibility", "visible");
      $(".cloned_photos .photo").css("visibility", "hidden");
    },
  
    change: function (e, ui) {
      $(".photos .photo:not(.exclude-me)").each(function () {
        var item = $(this);
        var clone = item.data("clone");
        clone.stop(true, false);
        var position = item.position();
        clone.animate(
          {
            left: position.left,
            top: position.top
          },
          200
        );
      });
    }
  });
  
/*-----------------------------------------------ПОДСЧИТЫВАНИЕ КОЛ-ВА СИМВОЛОВ В ОПИСАНИИ-------------------------------------------------------------*/
function charCount(){
  var element = document.getElementById('id_content').value.length; 
  document.querySelector('.desc_count').innerHTML = element + "/5000";
  if (element >= 5000){
    document.querySelector('.desc_count').style.color = '#9b111e';
    document.querySelector('.desc_count').style.opacity = '1';
  }
  else{
    document.querySelector('.desc_count').style.color = '#7d7d7d';
    document.querySelector('.desc_count').style.opacity = '0.6';
  }
}
/*------------------------------------------ПРОВЕРКА ЗАПОЛНЕННОЙ ФОРМЫ ADD------------------------------------------------------------------*/
// const form = document.getElementById('boardForm');

const photo1 = document.getElementById('photo1');
const photo1_img = document.getElementById('photo1_img');
const upload_button = document.querySelector('.upload_button');

const title = document.getElementById('id_title');
const salary = document.getElementById('id_price');
const workers_amount = document.getElementById('id_workers_amount');
const content = document.getElementById('id_content');
const author = document.getElementById('id_author_name');
const phone_number = document.getElementById('id_phone_number');
const email = document.getElementById('id_email');

const btn = document.querySelector('.submit_button');

document.getElementById('boardForm').addEventListener('submit', (e) => {
  btn.classList.add('button_loading_submit');
  // if(email.value === '' || email.value === null){
  //   e.preventDefault();
  //   btn.classList.remove('button_loading_submit');
  //   email.style.borderBottom = "1.6px solid rgba(255, 36, 0, 0.7)";
  //   window.scrollTo({
  //     top: 1000,
  //     behavior: 'smooth',});
  // }
  if(phone_number.value === '' || phone_number.value === null || !/^\+?3?8?(0\d{9})$/.test(phone_number.value)){
    e.preventDefault();
    btn.classList.remove('button_loading_submit');
    phone_number.style.borderBottom = "1.6px solid rgba(255, 36, 0, 0.7)";
    window.scrollTo({
      top: 1000,
      behavior: 'smooth',});
  }
  if(author.value === '' || author.value === null){
    e.preventDefault();
    btn.classList.remove('button_loading_submit');
    author.style.borderBottom = "1.6px solid rgba(255, 36, 0, 0.7)";
    window.scrollTo({
      top: 1000,
      behavior: 'smooth',});
  }
  
  if(salary.value === '' || salary.value === null || salary.value === 0){
    e.preventDefault();
    btn.classList.remove('button_loading_submit');
    salary.style.borderBottom = "1.6px solid rgba(255, 36, 0, 0.7)";
    window.scrollTo({
      top: 500,
      behavior: 'smooth',});
  }
  if(content.value === '' || content.value === null || content.value.length < 60){
    e.preventDefault();
    btn.classList.remove('button_loading_submit');
    content.style.border = "1.6px solid rgba(255, 36, 0, 0.7)";
    window.scrollTo({
      top: 770,
      behavior: 'smooth',});
  }


  // var upper_val = 0
  // for(var i=0; i < title.value.length; i++) {
  //   var char = title.value.charAt(i);

  //   if (char == char.toUpperCase())
  //   {
  //     upper_val++;
  //   }
  // }
  // if(upper_val >=25){
  //   e.preventDefault();
  //   btn.classList.remove('button_loading_submit');
  //   title.style.borderBottom = "1.6px solid rgba(255, 36, 0, 0.7)";
  //   window.scrollTo({
  //     top: 500,
  //     behavior: 'smooth',});
  // }
  if(title.value === '' || title.value === null || title.value.length < 10){
    e.preventDefault();
    btn.classList.remove('button_loading_submit');
    title.style.borderBottom = "1.6px solid rgba(255, 36, 0, 0.7)";
    window.scrollTo({
      top: 500,
      behavior: 'smooth',});
  }

  if (window.location.href.indexOf("add") > -1) { // Если мы находимся на странице добавления, а не изменения
    if(photo1_img_uploaded === false){
      e.preventDefault();
      btn.classList.remove('button_loading_submit');
      photo1.style.boxShadow = "0 0 4px black";
      upload_button.style.animation = "pulse 0.4s alternate infinite";
      window.scrollTo({
        top: 140,
        behavior: 'smooth',});
    }
  }
})
salary.addEventListener('keyup', function(){
  this.value = this.value.replace(/[^\d]/g, '');
  if (salary.value.length === 7){
    salary.blur();
  }
  else if (salary.value.length >= 7){
    this.value = this.value.replace('');
  }
});
if(workers_amount){
workers_amount.addEventListener('keyup', function(){
    this.value = this.value.replace(/[^\d]/g, '');
    if (workers_amount.value.length === 6){
      workers_amount.blur();
    }
    else if (workers_amount.value.length >= 6){
      this.value = this.value.replace('');
    }
  });
}
title.addEventListener('keyup', function(){
  if(title.value.length >= 10){
    title.style.borderBottom  = "0px solid rgba(0, 0, 0, 0)";
  }
});
if(content){
  content.addEventListener('keyup', function(){
    if(content.value.length >= 60){
      content.style.border = "0px solid rgba(0, 0, 0, 0)";
    }
  });
}

if(author){
  author.addEventListener('keyup', function(){
    if(author.value.length >= 1){
      author.style.border = "0.2px solid rgba(0, 0, 0, 0.5);";
    }
  });
}

if(phone_number){
  phone_number.addEventListener('keyup', function(){
    if(!/^\+?3?8?(0\d{9})$/.test(phone_number)){
      phone_number.style.border = "0.2px solid rgba(0, 0, 0, 0.5);";
    }
  });
}

// if(email){
//   email.addEventListener('keyup', function(){
//     if(email.value.length >= 1){
//       email.style.border = "0.2px solid rgba(0, 0, 0, 0.5);";
//     }
//   });
// }
/*------------------------------------------------------------------------------------------------------------*/
const select = document.querySelectorAll('.select');

// если массив не пустой, пробегаемся в цикле по каждому элементу
if (select.length) {
    select.forEach(item => {
        // достаем из текущей сущности .select__current
        const selectCurrent = item.querySelector('.select__current');
        
        item.addEventListener('click', event => {
            const text = event.target.innerText;
            selectCurrent.innerText = text;            
            item.classList.toggle('is-active');
        });
    })
}
/*---------------------------------------- DARK THEME --------------------------------------------------------------------*/
function getCookie(name) {
  var matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

var main = document.querySelector('.main');
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




/*-------------------------- ВЫТАСКИВАЕМ КОНТЕНТ ИЗ-ПОД PAGE_TITLE ПРИ АДАПТИВE ---------------------------------------------------------*/
var others_height = $('.page_title').outerHeight();
$('.add_header_h1').css('margin-top', others_height);
/*---------------------------------- ДВИГАЕМ НИЖНЮЮ ПОЛОСУ МЕНЮ  и PAGE_TITLE-------------------------------------------------------*/
$(document).ready(function() {
    var bottom_navigation = document.querySelector(".bottom_navigation");
    var page_title = document.querySelector(".page_title");
    var arr = [0];
    
    window.addEventListener('scroll', ()=>{
      let scrolled = window.scrollY;
      arr.push(scrolled);
      if(bottom_navigation || page_title){
        for(let i=arr.length-1; i<=arr.length; i++){
            if(arr[i-1] > arr[i]){
              bottom_navigation.classList.remove("bot_nav_hide");
              page_title.classList.remove("page_title_hide");
            }
            if(arr[i-1] < arr[i]){
              bottom_navigation.classList.add("bot_nav_hide");
              page_title.classList.add("page_title_hide");
            }        
        }
      }
    })
});
/*----------------------------------------- При нажатии на верхний блок перемещаемся вверх ------------------------------------------------------------------------*/
$( ".page_title" ).click(function() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',});
});


/*------------------------------------------ АДАПТИВ - УМЕНЬШЕНИЕ ИЗОБРАЖЕНИЯ ----------------------------------------------------------------*/
if(document.querySelector('.photo')){
  $(".photo").css("height", document.querySelector('.photo').clientWidth*0.8);
}
/*------------------------------------ ПРИ АДАПТИВЕ МОЖНО ПАЛЬЦЕМ ПЕРЕМЕЩАТЬ ЗАГРУЖЕННЫЕ ФОТО -----------------------------------------------------------------------*/
function touchHandler(event) {
  var touch = event.changedTouches[0];

  var simulatedEvent = document.createEvent("MouseEvent");
      simulatedEvent.initMouseEvent({
      touchstart: "mousedown",
      touchmove: "mousemove",
      touchend: "mouseup"
  }[event.type], true, true, window, 1,
      touch.screenX, touch.screenY,
      touch.clientX, touch.clientY, false,
      false, false, false, 0, null);

  touch.target.dispatchEvent(simulatedEvent);
}

function init() {
  document.addEventListener("touchstart", touchHandler, true);
  document.addEventListener("touchmove", touchHandler, true);
  document.addEventListener("touchend", touchHandler, true);
  document.addEventListener("touchcancel", touchHandler, true);
}

$(document).ready(function() {
init();
});