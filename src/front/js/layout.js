import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
// import { ToastContainer, toast } from "react-toastify";
import ScrollToTop from "./component/scrollToTop";
import { BackendURL } from "./component/backendURL";

import { Home } from "./views/Home.jsx";
import { Navbar } from "./component/Navbar.jsx";
import { Register } from "./component/Register.jsx";
import { Login } from "./component/Login.jsx";
import { GameForm } from "./component/GameForm.jsx"
import { GameView } from "./component/GameView.jsx";
import { Cart } from "./component/Cart.jsx"
import { MyGames } from "./component/MyGames.jsx";
import { UserGames } from "./component/UserGames.jsx";
import {SearchResults} from "./component/SearchResults.jsx";
import { Library} from "./component/Library.jsx"
import injectContext from "./store/appContext";
// import "react-toastify/dist/ReactToastify.css"



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
                {/* <ToastContainer
                position="top-center"
                autoClose={2000}
                hideProgressBar={false}
                newestOnTop
                closeOnClick={false}
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
                theme="dark"
                transition={Flip}
                /> */}
                    <Navbar />
                    <Routes>
                        <Route element={<Home />} path="/" />
                        <Route element={<h1>Not found!</h1>} />
                        <Route element={<Register/>} path="/register"/>
                        <Route element={<Login/>} path="/login"/>
                        <Route element={<GameForm/>} path="/submit-game"/>
                        <Route element={<GameView/>} path="/game/:theid"/>
                        <Route element={<SearchResults/>} path="/search-results"/>
                        <Route element={<Cart/>} path="/cart"/>
                        <Route element={<MyGames/>} path="/my-games"/>
                        <Route element={<UserGames/>} path="/user-games/:theid"/>
                        <Route element={<Library/>} path="/library"/>
                    </Routes>
                </ScrollToTop>
            </BrowserRouter>
        </div>
    );
};

export default injectContext(Layout);
