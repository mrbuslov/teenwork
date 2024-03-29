var bottom_navigation = document.querySelector(".bottom_navigation");
var cookies_mob = document.querySelector('.accept_cookie');
var arr = [0];


window.onload = function(){
  if (window.innerWidth < 1367){
    adaptive();
  }
};

window.onresize = function( event ) {
  if (window.innerWidth < 1367){
    adaptive();
  }
};
if (window.innerWidth < 1367){
  adaptive();
}
/*---------------------------------- ЗАМЕНЯЕМ PLACEHOLDER, если маленькое устройство -------------------------------------------------------*/
if (window.innerWidth < 480){
  if(window.location.pathname.includes('/uk/')){
    $('#id_title_content').attr('placeholder', 'Знайти');
  }
  else{
    $('#id_title_content').attr('placeholder', 'Поиск');
  }
}

/*----------------------------------  ЕСЛИ ЕСТЬ В ПУТИ НАШЕ КЛЮЧЕВОЕ СЛОВО, ТО ОТКРЫВАЕМ СТРОКУ ПОИСКА ---------------------------------- */
$(document).ready(function() {
  var url = window.location.href;
  if(url.includes('?open_search')){
    document.querySelector('.main_dark_search').classList.toggle('mds_show');
    document.querySelector('.search_field').classList.toggle('sf_show');
    document.querySelector('.search_arrow_down').classList.add('up');
  }
});

function adaptive(){
 /*---------------------------------- ДВИГАЕМ НИЖНЮЮ ПОЛОСУ МЕНЮ  и PAGE_TITLE-------------------------------------------------------*/
var page_title = document.querySelector(".page_title");
var arr = [0];
window.addEventListener('scroll', ()=>{
  let scrolled = window.scrollY;
  arr.push(scrolled);
  if(bottom_navigation || page_title){
    for(let i=arr.length-1; i<=arr.length; i++){
        if(arr[i-1] > arr[i]){
          bottom_navigation.classList.remove("bot_nav_hide");
          if(page_title){
            page_title.classList.remove("page_title_hide");
          }
        }
        if(arr[i-1] < arr[i]){
          bottom_navigation.classList.add("bot_nav_hide");
          if(page_title){
            page_title.classList.add("page_title_hide");
          }
        }        
    }
  }
})

  /*---------------------------------- РАБОТА СО СТРОКОЙ ПОИСКА -------------------------------------------------------*/
  var search = document.querySelector('.search_nav');
  search.onclick = function(){
    /* ПРОВЕРЯЕМ НА ГЛАВНОЙ ЛИ МЫ СТРАНИЦЕ */
    if(window.location.pathname=='/' || window.location.pathname=='/uk/'){
      document.querySelector('.main_dark_search').classList.toggle('mds_show');
      document.querySelector('.search_field').classList.toggle('sf_show');
      document.querySelector('.search_arrow_down').classList.add('up');
    }
    else{
      if(window.location.pathname.includes('/uk/')){
        window.location.href = '/uk/?open_search';
      }
      else{
        window.location.href = '/?open_search';
      }
    }
  }


  /*------------------------------------------------------- Убираем поле поиска, если щёлкаем вне него -------------------------------------------------------*/
  document.querySelector('.main_dark_search').onclick = function(){
    search.onclick();
    if(document.querySelector('.more_filters_field').style.display != 'none'){
      document.querySelector('.more_filters').onclick();
    }
  }
 
  /*---------------------------------- ...ОБЪЯВЛЕНИЕ -------------------------------------------------------*/
  $('.adt_n').each(function(i, obj) {
    $(obj).css('width', '100%');
    var letters_num = Number.parseInt(obj.offsetWidth/3.9); // сколько букв поместится в объявлении 
    if(obj.textContent.length > letters_num){
      var truncated = obj.textContent.trim().substring(0, letters_num) + "…";
      $(obj).text(truncated);
    }
  });
}


$( document ).ready(function() {
  if(window.location.href.includes('/uk/')){
    // $( ".adt_content" ).before( "<span class='adt_content_header'>Опис:</span>" );
  }
  else{
    $( ".adt_content" ).before( "<span class='adt_content_header'>Опис:</span>" );
  }
  $(document).on("click", ".adt_more_info", function(e){ 
    $(this).children('.adt_info').css('display', 'flex');
    document.querySelector('.adt_more_dark').classList.add('mds_show');
  });

  function close_advertisement_info(){
    $('.adt_info').css('display', 'none');
    document.querySelector('.adt_more_dark').classList.remove('mds_show');
    $('.adt_arrow_down').css('transform', 'rotate(45deg)');
  }
  
  $(document).on("click", ".adt_more_dark", function(){
    close_advertisement_info();
  }); 
  $(document).on("click", "#close_adt_more_info", function(e){
    e.stopPropagation();
    close_advertisement_info();
  });
  
})