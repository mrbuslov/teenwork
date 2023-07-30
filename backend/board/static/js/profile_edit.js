 /*----------------------------------  ЕСЛИ МЫ ПЕРЕШЛИ ПО ССЫЛКЕ ТЕЛЕГРАМ, ТО СПУСКАЕМСЯ ВНИЗ ---------------------------------- */
$(document).ready(function() {
  var url = window.location.href;
  if(url.includes('?tel')){
    window.scrollTo({
      top: 1000,
      behavior: 'smooth',
    });
  }
});

/*----------------------------------  AJAX TELEGRAM CHECKBOX---------------------------------- */
$(document).ready(function() {
  $('#tlg_checkbox').change(function(e) {
    e.preventDefault();
    var data = 'a';
    if ($(this).is(':checked')) {
      data = 'checked';
    }
    else{
      data = 'unchecked';
    }


    $.ajax({
        url: '/profile_edit/',
        type: 'POST',
        data: {'data':data},
        dataType: 'json',
        success: function(){
          if(document.getElementById('tlg_checkbox').checked === true){
            watch_tlg_show();
          }
        },
        error: function(){
          $('#tlg_checkbox').prop('checked', false)
        }
    });
  });

});

/*----------------------------------  ПРОВЕРЯЕМ TELEGRAM ПОЛЬЗОВАТЕЛЯ ---------------------------------- */
$(document).ready(function()
{
  var isTelegram = 'false'

  $.ajax({
    url: '/profile_edit/',
    type: 'POST',
    data: {'isTelegram':isTelegram},
    dataType: 'json',
    success: function(data){
      if(data === 'false'){
        $('#tlg_checkbox').prop('checked', false)
        check();
      }
      else if (data === 'true'){
        $('#tlg_checkbox').prop('checked', true)
        check();
      }
    },
    error: function(){
      $('#tlg_checkbox').prop('checked', false)
      check();
    }
  });
});


function open_delete_account() {
  document.querySelector('.pop_delete_account').style.display = 'flex';
}
function close_delete_account() {
  document.querySelector('.pop_delete_account').style.display = 'none';
}
// $(document).on('click', '.delete_btn', function () {
  $('.delete_btn').click(function () {
  console.log($(this))
  // $(this).parent('.adt').find('.pop_delete_adt').css('display', 'flex');
  $(this).find('.pop_delete_adt').css('display', 'flex');
});
$(document).on('click', '.close_pop_delete_adt', function () {
  $(this).closest('.adt').find('.pop_delete_adt').css('display', 'none');
});

/* -------------------------------- ЗАГРУЗКА ФОТО И СОХРАНЕНИЕ ЧЕРЕЗ 1 СЕК ------------------------------------------------------- */
if(document.getElementById('file')){
  document.getElementById('file').onchange = function() {
      if (this.files[0]){ // если выбрали файл
        document.getElementById('uploaded_image_name').innerHTML = this.files[0].name;
        //setTimeout(function() { document.getElementById('prof_btn').click();}, 1000);
        document.querySelector('.photo').style.opacity = '0.7';
        document.querySelector('.photo').style.filter = 'blur(2px)';
        document.getElementById('prof_btn').click();
      }
  };
}

function check(){
	const tlg_checkbox = document.getElementById('tlg_checkbox');
	const telegram_field = document.querySelector('.telegram_field');
	const info = document.querySelector('.info');
  if(tlg_checkbox){
    if (tlg_checkbox.checked) {
      telegram_field.style.background = "#fff";
      telegram_field.style.userSelect = "auto";
      info.style.visibility = "visible";
      
      document.getElementById('id_rubric').removeAttribute("disabled", "disabled");
      document.getElementById('id_age').removeAttribute("disabled", "disabled");
      document.getElementById('id_region').removeAttribute("disabled", "disabled");
      document.getElementById('id_city').removeAttribute("disabled", "disabled");
      document.getElementById('tlg_btn').removeAttribute("disabled", "disabled");
    }
    else {
      telegram_field.style.background = "rgba(0, 0, 0, 0.4)";
      telegram_field.style.userSelect = "none";
      info.style.visibility = "hidden";
      
      document.getElementById('id_rubric').setAttribute("disabled", "disabled");
      document.getElementById('id_age').setAttribute("disabled", "disabled");
      document.getElementById('id_region').setAttribute("disabled", "disabled");
      document.getElementById('id_city').setAttribute("disabled", "disabled");
      document.getElementById('tlg_btn').setAttribute("disabled", "disabled");
    }
  } 
}


function info_show(){
  document.querySelector('.info_text').style.visibility='visible';
  document.querySelector('.info_text').style.opacity='1';
}
function info_hide(){
  document.querySelector('.info_text').style.opacity='0';
  setTimeout(info_block_hide, 300);
}
function info_block_hide(){
  document.querySelector('.info_text').style.visibility='hidden';
}
var info = document.querySelector('.info');
if(info){
  info.onclick = function(){
    document.querySelector('.info_text').style.visibility='visible';
    document.querySelector('.info_text').style.opacity='1';
    setTimeout(info_hide_click, 3000);
  }
  function info_hide_click(){
    document.querySelector('.info_text').style.opacity='0';
    setTimeout(info_block_hide_click, 300);
  }
  function info_block_hide_click(){
    document.querySelector('.info_text').style.visibility='hidden';
  }
}



function watch_tlg_show(){
  document.querySelector('.watch_tlg').style.visibility='visible';
  document.querySelector('.watch_tlg').style.opacity='1';
  setTimeout(watch_tlg_hide, 3000)
}
function watch_tlg_hide(){
  document.querySelector('.watch_tlg').style.opacity='0';
  setTimeout(watch_tlg_block_hide, 300);
}
function watch_tlg_block_hide(){
  document.querySelector('.info_text').style.visibility='hidden';
}

/*---------------------------------------- ПРИ АДАПТИВЕ МЕНЯЕМ ЗАГОЛОВОК --------------------------------------------------------------------*/
if (document.querySelector('.watch_tlg') !== null){
  document.getElementsByClassName('watch_tlg')[0].innerHTML = "Вы можете перейти в Телеграм Бота через меню \"Другое\"";
}

/*---------------------------------------- ЕСЛИ ЕСТЬ АРХИВНОЕ ОБЪЯВЛЕНИЯ НАКЛАДЫВАЕМ ФОН --------------------------------------------------------------------*/
$(document).ready(function () {
  if($('.archive')){ // проверяем наличие элемента
    if (window.innerWidth > 1367){
      $('.archive').css('background', 'rgba(0, 0, 0, 0.4)');
    }
    else{
      $('.archive .container').css('background', 'rgba(0, 0, 0, 0.4)');
    }
    if(window.location.href.includes('/uk/')){
      // $('.archive .archive_btn a').text('Назад');
    }
    else{
      $('.archive .archive_btn a').text('Назад');
    }
  }
  if($('.edited')){ // проверяем наличие элемента
    if (window.innerWidth > 1367){
      $('.edited').css('background', 'rgba(0, 0, 0, 0.1)');
    }
    else{
      $('.edited .container').css('background', 'rgba(0, 0, 0, 0.1)');
    }
    if(window.location.href.includes('/uk/')){
      // $( ".edited .adt_a").after( "<span class='edited_adt'>Незабаром з'явиться на сайті</span>" );
    }
    else{
      $( ".edited .adt_a").each(function() {
        if ($(this).parents('.container_info').length) {
          $( this ).after( "<span class='edited_adt'>Незабаром з'явиться на сайті</span>" );
        }
      });
    }
  }
});