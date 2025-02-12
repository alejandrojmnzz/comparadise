import React from "react"
import "../../styles/tooltip.css"
import { useContext } from "react"
import { Context } from "../store/appContext"
import { useState } from "react"
import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

export function GamePreview() {
    const {store, actions} = useContext(Context)
    const navigate = useNavigate()
    const [relatedGame, setRelatedGame] = useState([])
    const [loading, setLoading] = useState(true)
    
    
    async function handleComparation() {
        for (let item of store.recentGames) {
            let response = await actions.multiQueryGame(item.auto_related_games[0])
            relatedGame.push(response)

        }
    }

    useEffect(() => {
        if (store.recentGames.length == 0) {
        actions.recentGames()
        }
        handleComparation()
    }, [store.recentGames])

    useEffect(() => {
        if (relatedGame) {
            setLoading(false)
        }
        console.log(relatedGame)
    }, [store.recentGames])

    return(
        <div className="container">
            <div className="row game-preview-row mt-3 d-flex justify-content-center">
                {
                loading ?

                <div className="d-flex justify-content-center align-items-center">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </div>
                </div>
                :
				store.recentGames.map((item, index) => {
					return (

						<div key={item.id}
                        className="game-preview col-12 col-md-6 col-lg-4 col-xl-3 col-xxl-2 mx-1 border border-secondary mb-4 p-0 d-flex position-relative"
                        onClick={() => navigate(`/game/${item.id}`)}
                        >
                        <div className="">
                        <div className="flip-card">
                        <div className="flip-card-inner">
                            <div className="flip-card-front">
                            <img src={item.cover_image} className="game-image"/>

                            </div>
                            <div>
                            <img src={item.cover_image} className="game-image"/>

                            </div>
                            <div className="flip-card-back">
                            <h2>{item.name}</h2>
                            <p>
                            {

                                item.genres.split(",").filter((genre, index) => index <= 2).map((genre, index) => {
                                    if ((item.genres.split(",").filter((genre, index) => index <= 2)).length == index + 1) {
                                        return (
                                            genre
                                        )
                                    }
                                    else {
                                        return (
                                            genre + ", "
                                        )
                                    }
                                })

                                }
                            </p>
                            <p>{item.summary}</p>
                            {/* <p>Release date: {item.release_date}</p> */}
                            {
                                
    
                           
                        <img src={`https://images.igdb.com/igdb/image/upload/t_1080p/${relatedGame[index]?.cover?.url?.split("/")[7]}`} className="preview-comparation-image"/>
                           }
                         {
             
                                console.log(relatedGame)
                               }
                        </div>
                        </div>
                        </div>
                            {/* <div className="tooltip d-flex">
                                <div className="tooltip-bg pb-2">
                                    <h5 className="d-flex justify-content-center m-0">{item.name}</h5>
                                    <span>{item.genres}</span>
                                    <img src={item.cover_image} className="tooltip-game-image rounded"/>
                                    <span className="mt-1"><b>Release Date:</b> {item.release_date}</span>
                                    <br></br>
                                </div>
                                <div className="related-games-tooltip d-flex justify-content-center">
                                    <div className="related-games-preview">
                                        <span><b>Related Games</b></span>
                                    </div>
                                 </div>
                            </div> */}
                        </div>
                        </div>
                        
					)
				})
			    }
            </div>
        </div>
    )
}