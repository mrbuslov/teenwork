function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

// ---------------------------------------- Загрузка последних сообщений чатов -----------------------------------------------------
$(document).ready(function(){
    $('.room_id').each(function(e){
        var room_id = $(this).val();
        var msg_field = $(this).siblings('.sms').children('.sms_name_chat');

        $.ajax({
            url: '/chat/get_last_msg/',
            type: 'get',
            data: {
                'room_id': room_id,
            },
            success: function(msg){
                msg_field.text(msg);
            },
            dataType: 'json',
            async: false,
        });
    });
});




/*------------------------------------------------- CHATS ---------------------------------------------------------*/

/*-------------------------- ВЫТАСКИВАЕМ КОНТЕНТ ИЗ-ПОД PAGE_TITLE ПРИ АДАПТИВE ---------------------------------------------------------*/
var others_height = $('.page_title').outerHeight();
$('.chats_search_field').css('margin-top', others_height);

/*-------------------------- Поиск чата ---------------------------------------------------------*/

//Для того, чтобы не было значения в инпуте
window.addEventListener("load",function(){
if(document.getElementById('searchInput')){
    document.getElementById('searchInput').value = '';
}
});
$(document).ready(function(){
$("#searchInput").keyup(function() {
var searchInput = $(this).val();
// if(searchInput === ''){
//     document.location.reload();
// }
    
$.ajax({
    url: '/chat/search_chats/',
    data: {
        'searchInput': searchInput
    },
    success: searchSuccess,
    dataType: 'json'
});

});
});


function searchSuccess(data)
{
var adts = data['adts'];
var participants = data['participants'];
var last_msg = data['last_msg'];
data = data['rooms'];
if(data.length === 0){
    document.getElementById('sms_field').innerHTML = "<h3 style='font-weight: normal;text-align: center;'>Мы не смогли ничего найти( </h3>";
}
else{
    document.getElementById('sms_field').innerHTML = "";

    $.each(data,function(index,value){
        var arr = [];
        var chat = "";

                
        chat = "<a href=\"/chat/"+ value['name'] +"/\" id=\"sms_a\">"+
            "<span class='sms_number'>"+ (index + 1) +"</span>"+
            "<div class='sms'>"+
                "<span class='adt_name_chat'>"+
                    adts[index]+
                "</span>"+
            " <span class='sender_name_chat'>"+
                    participants[index]+
                "</span>"+
                "<span class='sms_name_chat'>"+
                    last_msg[index]+
                "</span>"+
            "</div>"+
        "</a> ";
        
        arr.push(chat);
        
        var data = JSON.stringify(arr);
        data = JSON.parse(data);
        data.forEach(element => {
            document.getElementById('sms_field').innerHTML += element;
        });
    });
}
}








  // ---------------------------------------- ajax загрузка сообщений -----------------------------------------------------
  var count = 1;
  var this_user = $('#sender').val();

  if(document.getElementById('room_name')){
    var room_name = document.getElementById('room_name').value;
    window.onload = function() {
      setInterval(function(){
        $.ajax({
          type: 'GET',
          url: "/chat/getMessages/"+room_name+'/',
          data: {
            'last_msg':$('.message_val:last').text(),
          },
          success: function(response){
            var days = []; // для того, чтобы писать новый день новых сообщений

            if(response !== '"no_msgs"'){
              $("#messages_field").empty();
              $.each(response['messages'],function(index,value){
                var options = {
                  timezone: 'UTC',
                  hour: 'numeric',
                  minute: 'numeric',
                };
                var day_options = {
                  month: 'long',
                  day: 'numeric',
                  timezone: 'UTC',
                };

                var published = new Date(value['date']).toLocaleString("uk", options);
                if(window.location.pathname.includes('/en/')){
                var published_day = new Date(value['date']).toLocaleString("en", day_options);
                }else{
                var published_day = new Date(value['date']).toLocaleString("uk", day_options);
                }
                var day = '';

                if(!days.includes(published_day)){
                  days.push(published_day);
                  day = '<div class="day">' + published_day + '</div>';
                }

                var temp = '';
                console.log(this_user)
                console.log(value)
                console.log(value['sender'])
                if (value['sender'] === this_user){
                  temp="<div class='message right'><div class='msg_area'><div class='message_val'>"+value['value'].replace(/\n/g,'<br>') +"</div><div class='message_time'>"+published+"</div></div></div>";
                }
                else{
                  temp="<div class='message'><div class='msg_area'><div class='message_val'>"+value['value']+"</div><div class='message_time'>"+published+"</div></div></div>";
                }
                
                $("#messages_field").append(day);
                $("#messages_field").append(temp);
                $("#messages_field").animate({ scrollTop: $('#messages_field').prop("scrollHeight")}, 0);
              });
            };
          },
          error: function(response){
            $("#messages_field").empty();
            if(window.location.pathname.includes('/uk/')){
              $("#messages_field").append('<div class="loading" role="status">Завантаження...</div>');
            }else{
              $("#messages_field").append('<div class="loading" role="status">Загрузка...</div>');
            }
          }
        }); 
      },1000);
    }
  }
  // ---------------------------------------- Отправление сообщения -----------------------------------------------------

  $(document).on('submit','#post-form',function(e){
    e.preventDefault();
    if (document.getElementById('message').value != ''){
      $.ajax({
        type:'POST',
        url:'/chat/send',
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data:{
          'sender':$('#sender').val(),
          'receiver':$('#receiver').val(),
          'room_name':$('#room_name').val(),
          'message':$('#message').val(),
        },
        success: function(data){
          
        },
        error: function(e){
          document.location.reload();
          alert('Попробуйте ещё раз');
        }
      });
    }
    document.getElementById('message').value = '';
  });

  $("#message").keypress(function (e) {
    if(e.which === 13 && !e.shiftKey) {
        e.preventDefault();
        $('#send_msg_room').click();
    }
  });

  // ---------------------------------------- Добавление работника -----------------------------------------------------

  $( ".add_worker" ).click(function(e) {
    e.preventDefault();

    $.ajax({
      url:'/chat/add_worker/',
      type: 'POST',
      async: false,
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      data: {
        'room_name':$('#room_name').val(),
      },
      success: function(data) {
        if(data === 'added'){
          document.querySelector('.add_worker').style.display = 'none';
          document.querySelector('.emp_data').style.width = '100%';
          document.getElementById('message').value = 'Спасибо за Ваш отклик, Вы приняты!';
          add_worker_help_text_show();
        }
        else if(data === 'expired'){
          alert('Вы добавили максимальное кол-во работников.\nВаше объявление добавлено в архив.')
        }
        else{
          alert('Попробуйте ещё раз');
        }
      },
      error: function(){
        alert('Попробуйте ещё раз');
      }
    });
});

/*--------------------------------------ПОКАЗЫВАЕМ ВСПОМОГАТЕЛЬНОЕ ОКНО ПОСЛЕ ДОБАВЛЕНИЯ РАБОТНИКА----------------------------------------------------------------------*/
function add_worker_help_text_show(){
document.querySelector('.add_worker_help_text').style.visibility='visible';
document.querySelector('.add_worker_help_text').style.opacity='1';
setTimeout(add_worker_help_text_hide, 5000);
}
function add_worker_help_text_hide(){
document.querySelector('.add_worker_help_text').style.opacity='0';
setTimeout(add_worker_help_text_block_hide, 600);
}
function add_worker_help_text_block_hide(){
document.querySelector('.add_worker_help_text').style.visibility='hidden';
}
/*---------------------------------- Добавляем "срелочку" для выхода из чата ------------------------------------------------------------*/
$( ".photo" ).before( '<a href="#" onclick="history.back();" class="come_back"><em class="arrow-back"></em></a>' );
