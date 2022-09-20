// Если мы хотим узнать, это телефон или комптютер
// if (('ontouchstart' in window) ||
//       (navigator.maxTouchPoints > 0) ||
//       (navigator.msMaxTouchPoints > 0)){console.log('phone')};

/*---------------------- Проверка на то, есть ли запрос на фильтрацию - для того, чтобы скрыть логотип -------------------------------------- */
$(document).ready(function() {
  var url = window.location.href;
  var logo_teenwork = document.querySelector('.logo_teenwork');
  var lines_container = document.querySelector('.lines_container');
  var age_main = document.querySelector('.age_main');
  if(url.includes('title_content') || url.includes('page=1')){
    logo_teenwork.style.display = "none";
    lines_container.style.display = "none";
    age_main.style.display = "none";
  }
});
/*------------------------------------------------РЕГИСТРАЦИЯ----------------------------------------------------------------------*/
function show_password_eye() {
    var x = document.getElementById("password");
    const show_psswrd = document.getElementById('show_psswrd');	

    if (x.type === "password") {
      x.type = "text";
      show_psswrd.classList.add('hide');
    } else {
      x.type = "password";
      show_psswrd.classList.remove('hide');
    }
}
function show_password_eye_registr() {
  var p = document.getElementById("password");
  const show_psswrd = document.getElementById('show_psswrd');	
  if (p.type === "password") {
    p.type = "text";
    show_psswrd.classList.add('hide');
  } else {
    p.type = "password";
    show_psswrd.classList.remove('hide');
  }
}

$(document).ready(function(){
  $("#registrationForm").on('submit', (function(e) {
    var username_error = document.getElementById('username_error_text').textContent;
    var email_error = document.getElementById('email_error_text').textContent;
    var phone_number_error = document.getElementById('phone_number_error_text').textContent;
    var password_error = document.getElementById('password_error_text').textContent;
    if(username_error !== '' || email_error !== '' || phone_number_error !== '' || password_error !== ''){
      e.preventDefault();
      document.querySelector('.button').classList.remove('button_loading');
    }
    else{
      document.querySelector('.button').classList.add('button_loading');
    }
  }));
});


$(document).ready(function(){
  $("#username").blur(function() {
    var username = $(this).val();
    if(username !== ''){
        const username_regex = /^[a-zA-Z0-9_]{4,}[a-zA-Z]+[0-9]*$/.exec(username); //^(?=.{4,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$
        $(this).val(username.toLowerCase());
        
        $.ajax({
            url: '/registration/',
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type: 'POST',
            data: {
            'username': username,
            },
            success: function(data) {
                if(data === 'username_taken'){
                    document.getElementById('username_error_text').innerHTML = 'Ник занят, пожалуйста, придумайте другой'
                }
                else if(username.includes(' ')){
                    document.getElementById('username_error_text').innerHTML = 'Ник должен быть без пробелов'
                }
                else if(username.length < 4 || username.length > 25){
                    document.getElementById('username_error_text').innerHTML = 'Ник должен быть > 4 и < 25 символов'
                }
                else if(!username_regex){
                    document.getElementById('username_error_text').innerHTML = 'Ник должен содержать латинские буквы'
                }
                else{
                    document.getElementById('username_error_text').innerHTML = ''
                }
            },
            error: function(e){
              e.preventDefault();
              document.location.reload();
            }
        });
      }
      else{
          document.getElementById('username_error_text').innerHTML = ''
      }

  });
  $( "#phone_number" ).blur(function() {
      var phone_number = $(this).val();
      if(phone_number !== ''){                
          $.ajax({
              url: '/registration/',
              headers: { "X-CSRFToken": getCookie("csrftoken") },
              type: 'POST',
              data: {
              'phone_num': phone_number,
              },
              success: function(data) {
                  if(data === 'phone_taken'){
                      document.getElementById('phone_number_error_text').innerHTML = 'Кажется, такой телефон мы где-то видели -_-'
                  }
                  else if(!/^\+?3?8?(0\d{9})$/.exec(phone_number)){
                      document.getElementById('phone_number_error_text').innerHTML = 'Проверьте ещё раз, пожалуйста'
                  }
                  else{
                      document.getElementById('phone_number_error_text').innerHTML = ''
                  }
              },
              error: function(e){
                e.preventDefault();
                document.location.reload();
              }
          });
      }
      else{
          document.getElementById('phone_number_error_text').innerHTML = ''
      }
  });

  $( "#email" ).blur(function() {
      var email = $(this).val();
      if(email !== ''){                
          $.ajax({
              url: '/registration/',
              headers: { "X-CSRFToken": getCookie("csrftoken") },
              type: 'POST',
              data: {
              'email': email,
              },
              success: function(data) {
                  if(data === 'email_taken'){
                      document.getElementById('email_error_text').innerHTML = 'Кажется, такой email мы где-то видели -_-'
                  }
                  else if(!/^\S+@\S+\.\S+$/.exec(email)){
                      document.getElementById('email_error_text').innerHTML = 'Проверьте ещё раз, пожалуйста'
                  }
                  else{
                      document.getElementById('email_error_text').innerHTML = ''
                  }
              },
              error: function(e){
                e.preventDefault();
                document.location.reload();
              }
          });
      }
      else{
          document.getElementById('email_error_text').innerHTML = ''
      }
  });

  $( "#password" ).blur(function() {
      var password = $(this).val();
      if(password !== ''){          
        if(document.getElementById('password_error_text')){      
          if(password.length < 4){
            document.getElementById('password_error_text').innerHTML = 'Мы не хотим, чтобы Вас взломали, допишите пару букв'
          }
          else{
            document.getElementById('password_error_text').innerHTML = ''
          }
      }
      else{
        document.getElementById('password_error_text').innerHTML = ''
      }
    }
  });
});

if(document.querySelector('.agree_checkbox')){
  document.querySelector('.button').style.cursor = 'auto';
  document.querySelector('.button').style.background = '#1e83b1';
  document.querySelector('.button').style.opacity = '0.8';
  document.querySelector('.button').setAttribute("disabled", "disabled");

  document.querySelector('.agree_checkbox').onclick = function(){
    if (document.querySelector('.agree_checkbox').checked) {
      document.querySelector('.button').removeAttribute("disabled", "disabled");
      document.querySelector('.button').style.cursor = 'pointer';
      document.querySelector('.button').style.background = '#03a9f4';
      document.querySelector('.button').style.opacity = '1';
    }
    else {
      document.querySelector('.button').setAttribute("disabled", "disabled");
      document.querySelector('.button').style.cursor = 'auto';
      document.querySelector('.button').style.background = '#1e83b1';
      document.querySelector('.button').style.opacity = '0.8';
    }
  }
}
/*------------------------------------------------LOGIN----------------------------------------------------------------------*/
$(document).ready(function(){
  $("#loginForm").on('submit', function(e) {
    var email_error = document.getElementById('email_error_text').textContent;
    
    if(email_error !== ''){
      e.preventDefault();
      document.querySelector('.button').classList.remove('button_loading');
    }
    else{
      document.querySelector('.button').classList.add('button_loading');
    }
  });
});
$(document).ready(function(){
  $( "#email_login" ).blur(function() {
    var email_login = $(this).val();
    if(email_login !== ''){    
        $(this).val(email_login.toLowerCase());
        
      $.ajax({
        url: '/login/',
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type: 'POST',
        data: {
        'email_login': email_login,
        },
        success: function(data) {
          if(data === 'not_active'){
            document.getElementById('email_error_text').innerHTML = 'Проверьте почту, чтобы активировать аккаунт'
          }
          else if(data === 'blocked'){
            document.getElementById('email_error_text').innerHTML = 'К сожалению, Ваш профиль заблокирован. Обратитесь к администрации'
          }
          else if(data === 'not_exists'){
            document.getElementById('email_error_text').innerHTML = 'Для начала зарегестрируйтесь'
          }
          else{
            document.getElementById('email_error_text').innerHTML = ''
          }
        },
        error: function(e){
          e.preventDefault();
          document.location.reload();
        }
      });
    };
  });
});
/*------------------------------------------------ВЫПАДАЮЩИЙ СЛАЙДЕР ----------------------------------------------------------------------*/

var elem = document.querySelector(".test");
var arr = [0];

window.addEventListener('scroll', ()=>{
    let scrolled = window.scrollY;
    arr.push(scrolled);

    for(let i=arr.length-1; i<=arr.length; i++){
      if(arr[i-1] > arr[i]){
        if(elem){
          elem.classList.remove("hide");
        }
      }
      if(arr[i-1] < arr[i]){
        if(elem){
          elem.classList.add("hide");
        }
      }        
    }
})
//////////////////////////////////////// ДОПОЛНИТЕЛЬНОЕ ПОЛЕ ПОИСКА ВЫДВИГАЮЩЕЕСЯ МЕНЮ ///////////////////////////////////////////////////////////
var more_filters_field = document.querySelector('.more_filters_field');
if (more_filters_field !== null){
  document.querySelector('.more_filters').onclick = function(){
    if (more_filters_field.style.display === "none") {
      if (window.innerWidth < 1367){
        /*---------- Здесь мы берём реальную высоту элемента в auto, которую передадим adaptive_timerId_up, чтобы красиво по содержимому плавно выехало  --------------- */
        var $el = $('.more_filters_field'); // $ Это якобы ссылка на объект, его репрезентация
        var tmp = $el.css('height');
        var actualHeight = $el.css('height', 'auto').height();
        $el.css('height', tmp); 
        actualHeight = actualHeight+'px';
        /*------------------------- */
        $el.css('height') // это я оставил, потому что почему-то без этого оно плавно не выезжает о_о


        document.querySelector('.search_arrow_down').classList.remove('up');
        more_filters_field.style.display = "inline-block";

        setTimeout(adaptive_timerId_up(actualHeight), 1);
      }
      else{
        document.querySelector('.search_arrow_down').classList.add('up');
        more_filters_field.style.display = "inline-block";
        setTimeout(timerId_down, 1);
      }
    } 
    else {
      if (window.innerWidth < 1367){
        document.querySelector('.search_arrow_down').classList.add('up');
        more_filters_field.style.height = "0px";
        setTimeout(timerId_up, 600);
      }
      else{
        document.querySelector('.search_arrow_down').classList.remove('up');
        more_filters_field.style.height = "0px";
        setTimeout(timerId_up, 600);
      }
    }
  }
  function timerId_down() { 
    more_filters_field.style.height = "200px";}
  function adaptive_timerId_up(height) { 
    more_filters_field.style.height = height;}
  function timerId_up(){
    more_filters_field.style.display = "none";}
}

/*--------------------------------------------РЕГИОН И ГОРОД----------------------------------------------------------------*/
$("#id_region").change(function () {
  var url = $("#searchForm").attr("data-branches-url");  
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


// -------------------------------------- Дополнительный текст при наведении на ГАЛОЧКУ  ------------------------------------------------------------
$(document).on("mouseover",'.adt_name .tick', function () {
  console.log('hover')
  $(this).parent().find('.tick_text').css('opacity', 1);
  $(this).parent().find('.tick_text').css('visibility', 'visible');
});
$(document).on("mouseleave",'.adt_name .tick', function () {
  $(this).parent().find('.tick_text').css('opacity', 0);
});
/*-------------------------------------------- OTHERS PAGE адаптив ----------------------------------------------------------------*/
var page_title = document.querySelector('.page_title span');
if(page_title){
  page_title.onclick = function(){
    window.scrollTo({
      top: 0,
      behavior: 'smooth',});
  }
}

/*-- ВЫТАСКИВАЕМ КОНТЕНТ ИЗ-ПОД PAGE_TITLE ---------*/
var others_height = $('.page_title').outerHeight();
$('.others_list').css('margin-top', others_height);

var main = document.querySelector('.main');

const theme_checkbox = document.getElementById('theme_checkbox');
function theme_checkbox_check(){
	if (theme_checkbox.checked) {
		document.cookie = "theme=dark; path=/; max-age=2592000; samesite=lax";
    main.classList.add('dark');

    $("html").addClass("dark_scroll");
    $("body").addClass("dark_scroll");
	}
	else {
		document.cookie = "theme=light; path=/; max-age=2592000; samesite=lax";
    main.classList.remove('dark');

    $("html").removeClass("dark_scroll"); // СМЕНА ЦВЕТА ПОЛОСЫ ПРОКРУТКИ
    $("body").removeClass("dark_scroll");
	}
}

function getCookie(name) {
  var matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

if(getCookie('theme') === 'dark'){
  if(theme_checkbox){
    theme_checkbox.checked = true;
  }
}
else if(getCookie('theme') === 'light'){
  if(theme_checkbox){
    theme_checkbox.checked = false;
  }
}


/*-------------------------------------------- "ОТКРЫВАЕМ" ДОП ИНФО НА ГЛАВНОЙ СТРАНИЦЕ ----------------------------------------------------------------*/
const elToggle = document.querySelector('.adt_arrow_down_div');
const elBlock = document.querySelector('.adt_more_info');
if(elToggle){
  $(document).on("click", ".adt_arrow_down_div", function(e){ // для динамически созданного элемента
    console.log('asd')
    if($(this).parent().css('height') !== '20px'){
      $(this).parent().css('height', '20px');
      $(this).children().css('transform', 'rotate(45deg)')
    }
    else{
      $(this).parent().css('height', 'auto');
      $(this).children().css('transform', 'rotate(-135deg)')
    }
  });
}
/*-------------------------------------------- ЗАГРУЗКА AJAX ОБЪЯВЛЕНИЙ НА INDEX ----------------------------------------------------------------*/
$(document).ready(function(){   
  if(document.querySelector('.adt')){
    let not_scrolled = false;
    var adts_length = $('.adt').length;
    $(window).scroll(function() {
      var scroll = $(window).scrollTop() + $(window).height();
      var last_el = $('.adt_container').children().last(); // последний .adt
      var offset = last_el.offset().top // конец эл: var offset = last_el.offset().top + last_el.height();
      var new_adts_length = $('.adt').length;

      if(window.screen.width >= 1367 && new_adts_length > 15 || window.screen.width <= 1367){
          if(new_adts_length > adts_length){
            not_scrolled = true;
            adts_length = new_adts_length;
          }
      }

      if (scroll > offset && not_scrolled) {
        $("#load_main").click();
        not_scrolled = false;
      }
    });


    $("#load_main").on('click',function(){
        adts_arr = [];
        var lang = '';
        var btn_text = $("#load_main").text();
        $(".adt_a").each(function() {
            adts_arr.push($(this).attr('href'));
        });

        if(window.location.href.includes('/uk/')){
          lang = 'uk';
        }
        else{
          lang = 'ru';
        };

        $.ajax({
            url:"/load_more/",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            type:'post',
            data:{
              'adts_arr':adts_arr,
              'lang':lang,
              'what_user_searches':window.location.href.substring(window.location.href.lastIndexOf('?')),
            },
            dataType:'json',
            beforeSend:function(){
                $("#load_main").addClass('disabled').text('...');
            },
            success:function(res){
                var _html='';
                var json_data=$.parseJSON(res.posts);
                $.each(json_data,function(index,data){
                _html+='<div class="adt">\
        <div class="container">\
            <a href="'+data.fields.adt_url+'" class="adt_a">\
                <div class="adt_image_block">\
                    <img class="adt_image zoom" src="'+data.fields.image1+'" alt="'+data.fields.rubric+':'+data.fields.title+'">	\
                </div>\
                <span class="adt_name"> <span class="adt_n">'+data.fields.title+'</span>';
                    if(data.fields.author_official){
                        _html+= '<div class="tick">\
                            <div class="tick_right"></div>\
                            <div class="tick_left"></div>\
                        </div>\
                        <span class="tick_text">'+data.fields.tick_text+'</span>';
                    };
                _html+='</span> \
            </a>\
            <span class="adt_salary">'+data.fields.price+' '+data.fields.currency+'</span>\
            <br>\
                <span class="adt_age">'+data.fields.age+'</span>\
            <br>\
            <span class="adt_rubric">'+data.fields.rubric+'</span>\
            <br>\
            <span class="adt_city">'+data.fields.city+'</span>\
            <br>\
            <span class="adt_created">'+data.fields.published+'</span>\
            <div class="heart"> <a href="'+data.fields.fav_url+'">';
                if(data.fields.user_in_favourites){
                    _html+= '<img src="/static/img/full_heart.svg" alt="">';
                }
                else{
                    _html+= '<img src="/static/img/heart.svg" alt="">';
                };
                _html+='</a> \
            </div>\
        <div class="adt_more_info">\
            <div class="adt_arrow_down_div"><em class="adt_arrow_down"></em></div> \
            <div class="adt_info">\
                <div id="close_adt_more_info">+</div>\
                <div class="adt_author_info">\
                    <span class="name">';
                        if(data.fields.user_url !=''){
                            _html+= '<a href="'+data.fields.user_url+'">'+data.fields.adt_username+'</a>';
                        }
                        else{
                            _html+= data.fields.adt_username+'<span style="color: white; padding: 3px; background: #06b006; border-radius: 5px;">24h</span>';  
                        };
                    _html+='</span>\
                    <span class="phone_n_span">'+data.fields.phone_num_name+': <span class="phone_number">'+data.fields.phone_number+'</span></span> \
                    <span class="email_span">Email: <span class="email">'+data.fields.email+'</span></span>            \
                </div>\
                <div class="adt_content">'+data.fields.content+'</div>\
            </div>\
        </div>\
    </div>\
    </div>'
                });
                $(".adt_container").append(_html);
                var total_res=$(".adt").length;
                if(total_res == res.total_result){
                    $("#load_main").remove();
                }else{
                    $("#load_main").removeClass('disabled').text(btn_text);
                }
            }
        });
    });
  }
});