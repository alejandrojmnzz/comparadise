import React from "react";
import { NavLink } from "react-router-dom";
import { useContext } from "react";
import { Context } from "../store/appContext";

export function Navbar() {
    const {store, actions} = useContext(Context)
    
    function logOut() {
        localStorage.clear()
        actions.logout()
    }
    return (
        <>
            <div className="container">
                <div className="d-flex navbar">
                    <div className="justify-content-center search-content" role="search">
                        <input className="form-control me-2" type="search"  placeholder="Search" aria-label="Search"/>
                        <button className="btn btn-outline-success" type="submit">Search</button>
                    </div>

                    <div className="justify-content-end pt-2">
                    {
                    store.token == null ?
                    <NavLink to="/login" className="btn btn-primary">Log In</NavLink>
                    :
                    <button className="btn btn-primary" onClick={logOut}>Log Out</button>
                    }
                    </div>
                </div>
            </div>
        </>
    )
};