import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";
import { BackendURL } from "./component/backendURL";

import { Home } from "./views/Home.jsx";
import { Navbar } from "./component/Navbar.jsx";
import { Register } from "./component/Register.jsx";
import { Login } from "./component/Login.jsx";
import { GameForm } from "./component/GameForm.jsx"
import { GameView } from "./component/GameView.jsx";
import injectContext from "./store/appContext";


//create your first component
const Layout = () => {
    //the basename is used when your project is published in a subdirectory and not in the root of the domain
    // you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
    const basename = process.env.BASENAME || "";

    if(!process.env.BACKEND_URL || process.env.BACKEND_URL == "") return <BackendURL/ >;

    return (
        <div>
            <BrowserRouter basename={basename}>
                <ScrollToTop>
                    <Navbar />
                    <Routes>
                        <Route element={<Home />} path="/" />
                        <Route element={<h1>Not found!</h1>} />
                        <Route element={<Register/>} path="/register"/>
                        <Route element={<Login/>} path="/login"/>
                        <Route element={<GameForm/>} path="/submit-game"/>
                        <Route element={<GameView/>} path="/game/:theid"/>
                    </Routes>
                </ScrollToTop>
            </BrowserRouter>
        </div>
    );
};

export default injectContext(Layout);
