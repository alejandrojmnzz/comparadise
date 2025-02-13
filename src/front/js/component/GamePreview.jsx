import React from "react"
import "../../styles/tooltip.css"
import { useContext } from "react"
import { Context } from "../store/appContext"
import { useState } from "react"
import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

export function GamePreview() {
    const { store, actions } = useContext(Context)
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

    return (
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
                                    className="game-preview col-12 col-md-6 col-lg-4 col-xl-3 col-xxl-2 mx-1 border border-dark mb-4 p-0 d-flex position-relative"
                                    onClick={() => navigate(`/game/${item.id}`)}
                                >
                                    <div className="">
                                        <div className="flip-card">
                                            <div className="flip-card-inner border border-secondary">
                                                <div className="flip-card-front">
                                                    <img src={item.cover_image} className="game-image" />

                                                </div>
                                                <div>
                                                    <img src={item.cover_image} className="game-image" />

                                                </div>
                                                <div className="flip-card-back d-flex flex-column justify-content-between">
                                                    <div>
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
                                                    </div>

                                                    <div>
                                                        <p><b>Release date:</b> {item.release_date}</p>
                                                    </div>

                                                </div>
                                            </div>
                                        </div>

                                    </div>
                                </div>

                            )
                        })
                }
            </div>
        </div>
    )
}