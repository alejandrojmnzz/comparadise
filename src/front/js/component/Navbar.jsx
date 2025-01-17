import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import { useContext } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";

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

    const handleSearchChange = async(event) =>{
        const searchText = event.target.value;
        setQuery(searchText);

        if (searchText.length > 0) {
            
            try{
                const response = await fetch('${process.env.BACKEND_URL}/api/games/search?query=${searchText}');
                
                if (response.ok){
                    const data = await response.json();
                    setSuggestions(data);
                } 
                else {
                    console.error("No search results");
                    setSuggestions([]);
                }
            }
            catch (error) {
                console.error("Error", error);
                setSuggestions([]);
            }
        }
        else {
            setSuggestions([]);
        };

        const handleSearch = async () =>{
            if (query.trim() ==="") {
                alert ("Please enter something");
                return;
            }

            try {
                const response = await fetch (`${process.env.BACKEND_URL}/games-search?query=${query}`)
                
                if (response.ok) {
                    const data = await response.json();
                    setSuggestions(data);
                }
                else {
                console.error("No search results found.");
                setSuggestions([]);
                } 
            }
            catch (error) {
                console.error("Error fetching results:", error);
            }
            finally {
                setIsLoading(false);
            }
        };

        const handleSuggestionClick = (game) => {
            setQuery(game.name);
            setSuggestions([]);
        };

    }
    return (
        <>
        <div className="navbar-color">
            <div className="container">
                <div className="d-flex navbar">
                    <div className="search container" role="search">
                        <input 
                        className="form-control me-2"
                        type="search"  
                        placeholder="Search for a game" 
                        value={query} 
                        onChange={handleSearchChange} 
                        aria-label="Search"
                        />
                        <button className="btn btn-outline-success" type="submit">Search</button>
                        {suggestions.length > 0 && (
                            <ul className="suggestions-list">
                                {suggestions.map((game) => (
                                    <li
                                    key={game.id}
                                    onClick={() => handleSuggestionClick(game)}
                                    style={{ cursor: "pointer"}}>
                                        {game.name}
                                    </li>
                                ))}
                            </ul>
                        )}

                    </div>

                    <div className="justify-content-end pt-2">
                    {
                    store.token == null ?
                    <NavLink to="/login" className="btn btn-primary">Log In</NavLink>
                    :
                    <>
                        <NavLink to="/submit-game" className="btn btn-primary me-2">Submit Game</NavLink>
                        <button className="btn btn-danger" onClick={logOut}>Log Out</button>
                    </>
                    }
                    </div>
                </div>
            </div>
        </div>
        </>
    )
};