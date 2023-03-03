import React, { useState, useEffect } from "react";
import "./App.css";

import Header from "./components/Header/Header";
import StorePage from "./components/StorePage/StorePage.jsx";

function App() {
  const KEY = "192b5aaccffb4dbca5e56084f0eab10a";
  const API = `https://api.rawg.io/api/games?key=${KEY}&page_size=6`;

  const gamesDataFetch = async (url) => {
    const response = await fetch(url, {
      method: "GET",
      credentials: "same-origin",
      mode: "cors",
      headers: {
        "User-Agent": "RAWG API Client",
        "Content-Type": "application/json",
        Authorization: `Token ${KEY}`,
      },
    });
    const data = response.json();
    return data;
  };

  const [gameProperty, setGameProperty] = useState([]);

  const [gamesPagination, setPagination] = useState({});

  useEffect(() => {
    const getGamesData = async () => {
      try {
        const games = await gamesDataFetch(API);
        const gameResult = games.results;
        console.log(games);
        setPagination(games);

        setGameProperty(gameResult);
      } catch (error) {
        console.error(error);
      }
    };
    getGamesData();
  }, []);

  const onPrevious = async () => {
    const games = await gamesDataFetch(gamesPagination.previous);
    const gameResult = games.results;
    setPagination(games);
    setGameProperty(gameResult);
  };
  const onNext = async () => {
    const games = await gamesDataFetch(gamesPagination.next);
    const gameResult = games.results;
    setPagination(games);
    setGameProperty(gameResult);
  };

  return (
    <React.Fragment>
      <Header></Header>
      <StorePage
        gameProperty={gameProperty}
        prev={gamesPagination.previous}
        next={gamesPagination.next}
        onPrevious={onPrevious}
        onNext={onNext}
      ></StorePage>
    </React.Fragment>
  );
}

export default App;
