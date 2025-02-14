import React, { useContext, useEffect, useState} from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";
import { toast, ToastContainer, Flip } from "react-toastify";
import "react-toastify/dist/ReactToastify.css"
import "../../styles/cart.css"

export function Cart() {
    const {store, actions} = useContext(Context);
    const navigate = useNavigate();

    useEffect(() =>{
        actions.fetchCart();
    }, []);

    console.log("Cart contents:", store.cart);

    async function handleRemoveFromCart(cartId) {
        const response = await actions.removeFromCart(cartId);

        if (response.success) {
            toast.success("Game removed from cart successfully!");
            actions.fetchCart();
        } else {
            toast.error("Failed to remove game from cart.");
        }
    }

    async function handlePurchase() {
        const response = await actions.purchaseGames();
        if (response.success) {
            toast.success("Purchase successful! You can view your games in the Library.");
            actions.fetchCart();
            setTimeout (() => navigate("/library"), 3000);
        } else {
            toast.error("Failed to complete purchase.");
        }
    }

    return (
        <div className="container">
            <h1 className="text-center">Your Cart</h1>
            <button className="btn btn-secondary mt-2 go-back-button" onClick={() => navigate(-1)}>
                <i class="fa-solid fa-rotate-left"></i>
                &nbsp; Go Back</button>
                <ToastContainer
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
                />
            {store.cart.length === 0 ? (
                <p className="text-center">Your cart is empty.</p>
            ) : (
                <div className="row">
                    {store.cart.map((item, index) => (
                        <div key={index} className="col-12 d-flex justify-content-between align-items-center border-bottom py-2">
                            <div className="d-flex align-items-center">
                                <img src={item.game?.cover_image} alt={item.game?.name} style={{ width: "50px", height: "50px", objectFit: "cover"}} className="me-3"/>
                                <p className="m-0">{item.game?.name}</p>
                            </div>
                            <button className="btn btn-danger" onClick={() => handleRemoveFromCart(item.id)}>Remove</button>
                        </div>
                    ))}

                    <div className="text-center mt-4">
                        <button className="btn btn-success" onClick={handlePurchase}>Purchase</button>
                    </div>
                </div>
            )}

            {/* {errorMessage && (
                <div className="alert alert-danger mt-3 text-center">
                    {errorMessage}
                </div>
            )}

            {successMessage && (
                <div className="alert alert-success mt-3 text-center">
                    {successMessage}
                </div>
            )} */}
        </div>
    );
}
