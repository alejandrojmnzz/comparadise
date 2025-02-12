import React, { useState } from "react";
import { useEffect } from "react";
import { Context } from "../store/appContext";
import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import "../../styles/my-games.css"


export function MyGames() {
    const { store, actions } = useContext(Context)
    const navigate = useNavigate()
    const [rating, setRating] = useState([])
    const [likes, setLikes] = useState([])
    const [reviews, setReviews] = useState([])
    const [loading, setLoading] = useState(true)


    async function handleRating() {
        for (let item of store.currentUserGames) {
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

    }

    async function handleLikes() {
        for (let item of store.currentUserGames) {
            let response = await actions.getAllGameLikes(item.id)
            likes.push(response)

        }

    }
    async function handleReviews() {
        for (let item of store.currentUserGames) {
            let response = await actions.getAllReviews(item.id)
            let numberOfReviews = 0
            for (let review of response) {
                numberOfReviews++
            }

            reviews.push(numberOfReviews)
        }
        setLoading(false)
    }
    useEffect(() => {
        if (store.currentUserGames == null) {
            actions.getCurrentUserGames()
        }
        if (store.currentUserGames != null) {
            handleRating()
            handleLikes()
            handleReviews()
        }

    }, [store.currentUserGames])

    return (

        <div className="container">
            <button className="btn btn-secondary mt-2 go-back-button" onClick={() => navigate(-1)}>
                <i class="fa-solid fa-rotate-left"></i>
                    &nbsp; Go Back</button>
            {
                loading ?

                <div className="d-flex justify-content-center align-items-center">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </div>
                </div>
                :
                <>
                    <div className="d-flex justify-content-center">
                        <h1>Your Games</h1>
                    </div>
                    <div className="row d-flex justify-content-center">

                        {store.currentUserGames &&
                            store.currentUserGames.map((item, index) => {
                                return (
                                    
                                    <div className="col-md-6 col-xl-4">
                                        <h2 className="my-games-titles">{item.name}</h2>
                                        <div key={index} className="d-flex align-items-center mb-5">

                                            <img src={item["cover_image"]} onClick={() => navigate(`/game/${item.id}`)} className="my-games-image" />
                                            {/* <div>{item["name"]}</div> */}
                                            <div className="game-stats">
                                                <div className="d-flex align-items-center h-100">
                                                    <div className="d-flex flex-column align-items-center">
                                                        <h5>Rating</h5>
                                                        <p>{rating[index]}</p>
                                                        <h5>Likes</h5>
                                                        <p>{likes[index]}</p>
                                                        <h5>Reviews</h5>
                                                        <p className="m-0">{reviews[index]}</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                )
                            })}
                    </div>
                </>
            }

        </div>
    )
}