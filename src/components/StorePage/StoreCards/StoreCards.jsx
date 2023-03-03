import React from "react";
import './StoreCards.css'

function StoreCards({gameName,gameImage}) {
    return (
        <div className="Store-Page__cards">
            <img  className="Store-Page__cards-img"  src={gameImage} alt={gameName}/>
            <h3 className="Store-Page__cards-price">$255</h3>
            <h3 className="Store-Page__cards-title" title={gameName}>{gameName}</h3>
        </div>
    )
}

export { StoreCards }