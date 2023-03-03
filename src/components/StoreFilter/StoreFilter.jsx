

import React from "react";
import './StoreFilter.css';
import { FaCircleNotch } from "react-icons/fa";
// import { MdKeyboardArrowRight } from "react-icons/md";


function StoreFilter() {
    return (
        <form className="Store-filter__form">
            <div className="Store-filter__container-search">
                <span className="Store-filter__circle"><FaCircleNotch /></span>
                <input type="search" className="Store-filter__input" placeholder="Search"></input>
            </div>
            <div className="Store-filter__containerButtons">
                <button className="Store-filter__button">Precio</button>
                <button className="Store-filter__button">Modo de juego</button>
                <button className="Store-filter__button">Género</button>
            </div>
        </form>
    )
}

export { StoreFilter }