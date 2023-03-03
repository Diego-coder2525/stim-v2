import React from "react";
import './StorePage.css';
import { StoreCards } from "../StoreCards/StoreCards";
import { StoreFilter } from "../StoreFilter/StoreFilter";


function StorePage() {
    return (
        <section className="Store-Page__section">
            <div className="Store-Page__container-filters">
                <h2 className="Stora-Page__title-filters">Filtrar por categorías</h2>
                <StoreFilter/>
            </div>
            <div className="Store-Page__container-games">
                <h2 className="Store-Page__games-filters">Filtrado por: <span>Juegos Populares</span></h2>
                <div className="Store-Page__container-cards">
                    <StoreCards/>
                    <StoreCards/>
                    <StoreCards/>
                    <StoreCards/>
                    <StoreCards/>
                    <StoreCards/>
                </div>
            </div>
        </section>
    )
}

export default StorePage;