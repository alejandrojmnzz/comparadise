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
                <div className="d-flex justify-content-end pt-2 navbar">
                    <div className="d-flex container-fluid bg-body-tertiary">

                    </div>

                    <div>
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