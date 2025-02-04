import React, { useContext, useEffect, useState} from "react";
import { Context } from "../store/appContext";

export function Cart() {
    const {store, actions} = useContext(Context);
    const [errorMessage, setErrorMessage] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);

    useEffect(() =>{
        actions.fetchCart();
    }, []);

    console.log("Cart contents:", store.cart);

    async function handleRemoveFromCart(cartId) {
        const response = await actions.removeFromCart(cartId);

        if (response.success) {
            setErrorMessage("Game removed from cart successfully!");
            setSuccessMessage(null);
            actions.fetchCart();
        } else {
            setSuccessMessage("Failed to remove game from cart.");
            setErrorMessage(null);
        }
    }

    return (
        <div className="container">
            <h1 className="text-center">Your Cart</h1>
            {store.cart.length === 0 ? (
                <p className="text-center">Your cart is empty.</p>
            ) : (
                <div className="row">
                    {store.cart.map((item, index) => (
                        <div key={index} className="col-12 d-flex justify-content-between aligns-items-center border-bottom py-2">
                            <div className="d-flex align-items-center">
                                <img src={item.game.cover_image} alt={item.game.name} style={{ width: "50px", height: "50px", objectFit: "cover"}} className="me-3"/>
                                <p className="m-0">{item.game.name}</p>
                            </div>
                            <button className="btn btn-danger" onClick={() => handleRemoveFromCart(item.id)}>Remove</button>
                        </div>
                    ))}
                </div>
            )}

            {errorMessage && (
                <div className="alert alert-danger mt-3 text-center">
                    {errorMessage}
                </div>
            )}

            {successMessage && (
                <div className="alert alert-success mt-3 text-center">
                    {successMessage}
                </div>
            )}
        </div>
    );
}
