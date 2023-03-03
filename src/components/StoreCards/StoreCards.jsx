import React from "react";


import portal2 from '../../assets/img/Portal2.jpg'
import './StoreCards.css';

function StoreCards() {
    return (
        <div className="Store-Page__cards">
            <img  className="Store-Page__cards-img" src={portal2} alt="Portal 2"/>
            <h3 className="Store-Page__cards-price">$255</h3>
            <h3 className="Store-Page__cards-title">Portal 2</h3>
        </div>
    )
}

export { StoreCards }