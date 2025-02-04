import React, { useState } from "react";
import { useEffect } from "react";
import { Context } from "../store/appContext";
import { useContext } from "react";
import { useNavigate } from "react-router-dom";


export function MyGames() {
    const {store, actions} = useContext(Context)
    const navigate = useNavigate()
    useEffect(() => {
        actions.getCurrentUserGames()
        if (store.currentUserGames != null) {
            actions.getUser(store.currentUserGames[0]["user_id"])
            }
    }, [])

    return (
        <>
            <div className="d-flex justify-content-center">
                <h1>{store.singleUser["name"]}'s Games</h1>
            </div>
            <div className="d-flex justify-content-center gap-3">

                {store.currentUserGames && 
                store.currentUserGames.map((item) => {
                    return (
                    <div>
                        <img src={item["cover_image"]} onClick={() => navigate(`/game/${item.id}`)} className="img-pointer"/>
                        <div>{item["name"]}</div>
                    </div>
                    )
                })}  
            </div>
        </>
    ) 
}