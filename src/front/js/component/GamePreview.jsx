import React from "react"
import "../../styles/tooltip.css"
import { useContext } from "react"
import { Context } from "../store/appContext"
import { useState } from "react"
import { useEffect } from "react"

export function GamePreview() {
    const {store, actions} = useContext(Context)
    
    useEffect(() => {
        actions.recentGames()
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
            <div className="row game-preview-row mt-3 ">
                {
				store.recentGames.map((item) => {
					return (
                        <>
						<div key={item.id}
                        className="game-preview col-12 col-md-6 col-lg-4 col-xl-3 col-xxl-2 border rounded px-2 mb-4 p-0 d-flex position-relative"
                        >
                            <img src={item.cover_image} className="game-image border rounded"/>
                            <div className="tooltip d-flex">
                                <div className="tooltip-bg pb-2">
                                    <h5 className="d-flex justify-content-center m-0">{item.name}</h5>
                                    <span>{item.genre}</span>
                                    <img src={item.cover_image} className="tooltip-game-image rounded"/>
                                    <span className="mt-1"><b>Release Date:</b> {item.release_date}</span>
                                    <br></br>
                                    <span><b>Rating:</b></span>
                                </div>
                                <div className="related-games-tooltip d-flex justify-content-center">
                                    <div className="related-games-preview">
                                        <span><b>Related Games</b></span>
                                    </div>
                                 </div>
                            </div>
     
                        </div>
                        
                      </>
					)
				})
			    }
            </div>
        </div>
    )
}