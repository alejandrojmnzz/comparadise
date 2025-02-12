import React, { use, useEffect, useState, useContext } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";

export function SearchResults() {
    const { store } = useContext(Context);

    // Ensures the component re-renders when search results change
    useEffect(() => {}, [store.searchResults]);

    return (
        <div className="container mt-5">
           <button className="btn btn-secondary mt-2 go-back-button" onClick={() => navigate(-1)}>
                <i class="fa-solid fa-rotate-left"></i>
                &nbsp; Go Back</button> 
            <h2>Search Results</h2>

            {store.searchResults.length === 0 ? (
                <p>No games found. Try a different search.</p>
            ) : (
                <ul className="list-group">
                    {store.searchResults.map((game) => (
                        <li key={game.id} className="list-group-item">
                            <h5>{game.name}</h5>
                            {game.cover_image && <img src={game.cover_image} alt={game.name} className="img-thumbnail" onClick={() => navigate(`/game/${item.id}`)}/>}
                            <p>Release Date: {game.release_date}</p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default SearchResults;