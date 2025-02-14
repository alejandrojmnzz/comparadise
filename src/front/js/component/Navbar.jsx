import React, { useState, useSyncExternalStore } from "react";
import { NavLink } from "react-router-dom";
import { useContext } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";
import ComParadise from "../../img/ComParadise.png"
import "../../styles/navbar.css"
import { toast, ToastContainer, Flip } from "react-toastify";
import "react-toastify/dist/ReactToastify.css"

export function Navbar() {
    const {store, actions} = useContext(Context)
    const [query, setQuery] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const navigate = useNavigate()

    function logOut() {
        localStorage.clear()
        actions.logout()
        navigate('/')
    }

    function goToMainPage() {
        navigate("/");
    }
    function goToCart() {
        navigate("/cart");
    }

    const handleSearchChange = async (event) => {
        const searchText = event.target.value;
        setQuery(searchText);

        if (searchText.length > 0) {
            try {
                const response = await fetch(`${process.env.BACKEND_URL}/games-search?query=${searchText}`);
                if (response.ok) {
                    const data = await response.json();
                    setSuggestions(data);
                } else {
                    console.error("No search results");
                    setSuggestions([]);
                }
            } catch (error) {
                console.error("Error", error);
                setSuggestions([]);
            }
        } else {
            setSuggestions([]);
        }
    };

    
    const handleSearch = async () => {
        if (query.trim() === "") {
            toast.info("Please enter something");
            return;
        }

        actions.fetchSearchResults(query);
        navigate("/search-results");

        setQuery("");
        setSuggestions("");
    };

    const handleKeyDown = (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            handleSearch();
            setSuggestions("");
        }
    };

    const handleClick = () => {
        handleSearch();
        setSuggestions("");
    };

    const handleSuggestionClick = (game) => {
        setQuery(""); 
        setSuggestions([]); 
        navigate(`/game/${game.id}`);
    };
    return (
        <div className="navbar navbar-expand-lg navbar-light bg-body-tertiary navbar-color">
            <div className="container-fluid d-flex justify-content-between align-items-center">
                
                    <button className="btn p-0" onClick={goToMainPage}>
                        <img className="logo-home" src="ComParadise.png" alt="Home"/>
                    </button>
                    
                <div className="d-flex align-items-center flex-grow-1 mx-3" role="search">
                    <input
                        className="form-control me-2 navbar-search-bar"
                        type="search"
                        placeholder="Search for a game"
                        value={query}
                        onChange={handleSearchChange}
                        onKeyDown ={handleKeyDown}
                        aria-label="Search"
                    />
                    <button className="btn btn-primary search-button" type="button" onClick={handleClick}>
                        Search
                    </button>

                        {suggestions.length > 0 && (
                            <ul className="suggestions-list list-group position-absolute bg-white shadow rounded">
                                {suggestions.map((game) => (
                                    <li 
                                    key={game.id} 
                                    className="list-group-item list-group-item-action"
                                    onClick={() => handleSuggestionClick(game)} 
                                    style={{ cursor: "pointer" }}>
                                        {game.name}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                    
                    <div className="d-flex align-items-center">
                        {store.token && (
                            <NavLink to="/submit-game" className="btn btn-primary submit-button">
                                <i class="fa-solid fa-rectangle-list"></i>
                                &nbsp; Submit Game</NavLink>
                        )}
                    <div class="dropdown">
                        <button class="btn dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fa-solid fa-bars"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end">
                        {store.token == null ? (
                            <>
                            <li>
                                <NavLink to="/login" className="dropdown-item">
                                <i class="fa-solid fa-right-to-bracket"></i>
                                &nbsp; Log In</NavLink>
                            </li>
                            <li>
                                <NavLink to="/register" className="dropdown-item">
                                <i class="fa-solid fa-id-card"></i>
                                &nbsp; Register</NavLink>
                                </li>
                            </>
                        ) : (
                            <>
                            <li>
                                <button className="dropdown-item" onClick={goToCart}>
                                <i class="fa-solid fa-cart-shopping"></i>
                                &nbsp; Cart {store.cart?.length > 0 && `(${store.cart.length})`}
                                </button>
                            </li>
                            <li><NavLink to="/library" className="dropdown-item">
                                <i class="fa-solid fa-compact-disc"></i>
                                &nbsp; Library</NavLink></li>
                            <li><NavLink to="/my-games" className="dropdown-item">
                            <i class="fa-solid fa-gamepad"></i>
                                &nbsp; My Games</NavLink></li>
                            <li><hr className="dropdown-divider"/></li>
                            <li><button className="dropdown-item" onClick={logOut}>
                                <i class="fa-solid fa-right-from-bracket"></i>
                                &nbsp; Log Out</button></li>
                        </> 
                      )}  
                        </ul>
                    </div>
                    </div>
                </div>
            </div>
    );
}

export default Navbar;