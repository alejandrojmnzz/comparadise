import React from "react";
import { NavLink } from "react-router-dom";

export function Navbar() {
    return (
        <>
            <div className="container">
                <div className="d-flex justify-content-end pt-2">
                    <NavLink to ="/register" className="btn btn-primary">Sign In</NavLink>
                </div>
            </div>
        </>
    )
}