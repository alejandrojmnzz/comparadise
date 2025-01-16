import React from "react";
import { NavLink } from "react-router-dom";
import { useContext } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";

export function Navbar() {
    const {store, actions} = useContext(Context)
    const navigate = useNavigate()

    function logOut() {
        localStorage.clear()
        actions.logout()
        navigate('/')
    }
    return (
        <>
        <div className="navbar-color">
            <div className="container">
                <div className="d-flex justify-content-end pt-2 navbar">
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
        </>
    )
};