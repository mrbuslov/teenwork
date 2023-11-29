import { NavLink } from "react-router-dom";
import classes from './NavBar.module.scss';

interface NavLinkProps {
  isActive: boolean;
};


// difference between NavLink and Link is that NavLink applies "active" attribute to link, if we're on that page
const Navbar = () => {
  const setActive = ({isActive}: NavLinkProps) => isActive ? classes.activeLink : "";
  return (
    <header>
      <NavLink to="/">
        <img 
          src="logo.svg" 
          className={classes.logo}
          alt="Teenwork service logo"
          title="Teenwork - work for teenagers and not only"
        />
      </NavLink>

      <div className={classes.langs}>
        <NavLink to="/" className={setActive}>English</NavLink>
        <NavLink to="/ru" className={setActive}>Русский</NavLink>
      </div>

          

    </header>
  )


//   <ul class="test_ul">
//   <li>
//   <div class="account"><div class="account_icon"> <img src="{% static 'img/profile.svg' %}" alt="">
//       {% if user.is_authenticated %}
//       {{user.username}}</div>
//       <div class="dropdown-content">
//       <a href="{% url 'account:profile_edit' %}">{% translate "Открыть профиль" %}</a>
//       <a href="{% url 'account:profile' %}">{% translate "Мои объявления" %}</a>
//       <a href="{% url 'chat:show_chats' %}">{% translate "Сообщения" %}</a>
//       <a href="{% url 'account:logout' %}">{% translate "Выйти" %}</a>
//       </div>
//       {% else %}
//       <a href="{% url 'account:login' %}">{% translate "Войти в профиль" %}</a></div>
//       {% endif %}
//   </div>
//   </li>

//   <li>
//   <div class="telegram">
//       <div>
//       <a href="{% url 'telegram_filter:get_unique_code' %}" class="tgrm_icon"> 
//           <img src="{% static 'img/telegram.svg' %}" alt="" class="telegram_icon">
//           Bot</a></div>
//       <div class="prompt_telegram_bot">Телеграм Бот</div>
//   </div>
//   </li>
  
//   <li>
//   <div class="add_post"><span class=add_cross>+</span><a href="{% url 'board:add' %}">{% translate "Добавить объявление" %}</a></div>
//   </li>

//   <li>
//   <a href="{% url 'account:favourite_list' %}" >
//       <img src="{% static 'img/full_heart.svg' %}" alt="" class="liked_posts">
//   </a>
//   </li>

//   <li><span class="toggle"></span></li>
// </ul>
// </div>

// <div class="accept_cookie">
// <div class="cookie_photo">
//   <img src="{% static 'img/cookie.svg'%}" alt="">
// </div>
// <span class="cookie_text">
//   {% translate "Мы будем использовать куки, чтобы запоминать Ваши предпочтения, менять тему сайта и многое полезное" %}
// </span>
// <div class="cookie_buttons">
//   <div class="cookie_know_more">
//       <a href="#"><span class="cookie_know_more_text">{% translate "Узнать больше" %}</span></a>
//   </div>
//   <button type="button" class="cookie_submit_button">{% translate "Принять" %}</button>
// </div>
// </div>


// <div class="try_24h">
// <div class="try_24h_photo">
//   <img src="{% static 'img/24h.svg'%}" alt="">
// </div>
// <span class="try_24h_text">
//   {% translate "Давайте опубликуем объявление без регистрации? Попробуйте, это бесплатно" %}
// </span>
// <div class="try_24h_buttons">
// <button type="button" class="try_24h_submit_button">{% translate "Окей" %}</button>
//   <div class="try_24h_know_more">
//   <a href="{% url 'board:how_24h_works' %}" target="_blank"><span class="try_24h_know_more_text">{% translate "Как это работает?" %}</span></a>
//   </div>
// </div>
// </div>
}

export default Navbar
