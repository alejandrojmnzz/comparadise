import React from "react"
import { useContext } from "react"
import { Context } from "../store/appContext"
import { useState } from "react"
import { useEffect } from "react"

export function GamePreview() {
    const {store, actions} = useContext(Context)
    
    useEffect(() => {
        actions.recentGames()
        console.log(store.recentGames)
    }, [])

    function hover(event) {
        return (
            <div className="border border-danger h-50 w-50">
                prueba
            </div>
        )
    }
    return(
        <div className="container">
            <div className="row game-preview-row justify-content-between mt-3">
                {
				store.recentGames.map((item) => {
					return (
                        <>
						<div key={item.id}
                        className="game-preview col-2 border rounded mx-2 mb-4">
                            <img src={item.cover_image}/>
                            
                        </div>

                      </>
					)
				})
			    }
            </div>
        </div>
    )
}