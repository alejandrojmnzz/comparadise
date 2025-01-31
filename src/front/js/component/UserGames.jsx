import React, { useState } from "react";
import { useEffect } from "react";
import { Context } from "../store/appContext";
import { useContext } from "react";
import { useNavigate, useParams } from "react-router-dom";


export function UserGames() {
    const {theid} = useParams()
    const {store, actions} = useContext(Context)
    const navigate = useNavigate()
    useEffect(() => {
        actions.getUserGames(theid)
    }, [])

    return (
        <>
            <div className="d-flex justify-content-center">
                <h1>{store.singleUser["name"]}'s Games</h1>
            </div>
            <div className="d-flex justify-content-center gap-3">

                {store.userGames && 
                store.userGames.map((item) => {
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