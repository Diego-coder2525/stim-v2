import React from "react";
import "./header.css";
import userIcon from "../../assets/ph_user-bold.svg";
function Header() {
  return (
    <header>
      <nav className="nav__container">
        <span className="logo"><a href="#">Stim_</a></span>
        <ul className="nav__container-list">
          <li>
            <a href="#" className="nav__container-list__links">
              tienda
            </a>
          </li>
          <li>
            <a href="#" className="nav__container-list__links">
              comunidad
            </a>
          </li>
          <li>
            <a href="#" className="nav__container-list__links">
              noticias
            </a>
          </li>
          <li>
            <a href="#" className="nav__container-list__links">
              ayuda
            </a>
          </li>
        </ul>
        <picture>
          <a href="#">
            <img src={userIcon} className="nav__container-user-icon"alt="user icon" />
          </a>
        </picture>
      </nav>
    </header>
  );
}

export default Header;
