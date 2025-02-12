import React, { useState } from "react";
import { useEffect } from "react";
import { Context } from "../store/appContext";
import { useContext } from "react";
import { useNavigate, useParams } from "react-router-dom";


export function UserGames() {
    const { theid } = useParams()
    const { store, actions } = useContext(Context)
    const [loading, setLoading] = useState(true)
    const [rating, setRating] = useState([])
    const navigate = useNavigate()

    async function handleRating() {
        for (let item of store.userGames) {
            let review = 0

            let allReviews = await actions.getAllReviews(item.id)
            for (let i of allReviews) {
                review = review + i.rating

            }
            if (review != 0) {
                review = review / allReviews.length
            }

            rating.push(Math.round(review))
        }
        setLoading(false)
    }

    useEffect(() => {
        actions.getUserGames(theid)
        actions.getUser(theid)
        handleRating()
    }, [])

    useEffect(() => {
        handleRating()
    }, [store.userGames])

    return (
        <>
                <div className="">
                    <button className="btn btn-secondary mt-2 ms-2 go-back-button" onClick={() => navigate(-1)}>
                            <i class="fa-solid fa-rotate-left"></i>
                                &nbsp; Go Back</button>
                    <div className="d-flex justify-content-center my-2">
                        <h1>{store.singleUser["name"]}'s Games</h1>
                    </div>
                    <div className="container p-0">
                        {store.userGames &&
                            store.userGames.map((item, index) => {
                                return (
                                    <div className="mb-4 border user-game-color px-4 pt-4 col-12 rounded" key={index}>
                                        <div className="row d-flex justify-content-between">

                                            <div className="col-sm-5 col-md-4 col-xl-3 p-0">
                                                <div className="d-flex justify-content-center">
                                                    <img src={item["cover_image"]} onClick={() => navigate(`/game/${item.id}`)} className="user-game" />
                                                </div>
                                                <div className="d-flex justify-content-center text-center mt-1">
                                                    <h3 className="user-games-title">{item["name"]}</h3>
                                                </div>
                                            </div>
                                            <div className="col-sm-10 col-md-8 col-xl-6 d-flex justify-content-center align-items-center">
                                                <div>
                                                    <div className="d-flex justify-content-center">
                                                        <img className="user-images" src={item.additional_images[0]} />
                                                        <img className="user-images" src={item.additional_images[1]} />
                                                    </div>
                                                    <div className="d-flex justify-content-center">
                                                        <img className="user-images" src={item.additional_images[2]} />
                                                        <img className="user-images" src={item.additional_images[2]} />
                                                    </div>
                                                    <div className="d-flex justify-content-center align-items-end fs-5 mt-3">
                                                        <p className="user-game-p-color">{item.summary}</p>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="col-sm-5 col-md-4 col-xl-3 d-flex flex-column justify-content-between">
                                                <div>
                                                    <h5 className="p-0 aspect-color">Genres</h5>
                                                    <p className="p-1 user-game-p-color">
                                                        {

                                                            item.genres.split(",").filter((genre, index) => index <= 4).map((genre, index) => {
                                                                if ((item.genres.split(",").filter((genre, index) => index <= 4)).length == index + 1) {
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
                                                    <h5 className="p-0 aspect-color">Game Modes</h5>
                                                    <p className="p-1 user-game-p-color">
                                                        {

                                                            item.modes.split(",").filter((mode, index) => index <= 4).map((mode, index) => {
                                                                if ((item.modes.split(",").filter((mode, index) => index <= 4)).length == index + 1) {
                                                                    return (
                                                                        mode
                                                                    )
                                                                }
                                                                else {
                                                                    return (
                                                                        mode + ", "
                                                                    )
                                                                }
                                                            })

                                                        }
                                                    </p>
                                                    <h5 className="p-0 aspect-color">Themes</h5>
                                                    <p className="p-1 user-game-p-color">
                                                        {

                                                            item.themes.split(",").filter((theme, index) => index <= 4).map((theme, index) => {
                                                                if ((item.themes.split(",").filter((theme, index) => index <= 4)).length == index + 1) {
                                                                    return (
                                                                        theme
                                                                    )
                                                                }
                                                                else {
                                                                    return (
                                                                        theme + ", "
                                                                    )
                                                                }
                                                            })

                                                        }
                                                    </p>
                                                    <h5 className="p-0 aspect-color">Player Perspectives</h5>
                                                    <p className="p-1 user-game-p-color">
                                                        {

                                                            item.player_perspective.split(",").filter((perspective, index) => index <= 4).map((perspective, index) => {
                                                                if ((item.player_perspective.split(",").filter((perspective, index) => index <= 4)).length == index + 1) {
                                                                    return (
                                                                        perspective
                                                                    )
                                                                }
                                                                else {
                                                                    return (
                                                                        perspective + ", "
                                                                    )
                                                                }
                                                            })

                                                        }
                                                    </p>
                                                </div>
                                                <div className="user-game-rating">
                                                    <span className=""><b>Rating: {rating[index]}</b></span>

                                                </div>
                                            </div>
                                        </div>

                                    </div>
                                )
                            })}
                    </div>
                </div>
        </>
    )
}