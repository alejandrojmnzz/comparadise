import React, { useEffect, useContext, useState } from "react";
import { NavLink, useParams, useRoutes } from "react-router-dom";
import { Context } from "../store/appContext";

export function GameView() {
    const { theid } = useParams()
    const { store, actions } = useContext(Context)
    const [autoRelatedGames, setAutoRelatedGames] = useState()
    const [review, setReview] = useState({
        "rating": 0,
        "review": "",
        "game_id": null
    })
    const [userReview, setUserReview] = useState()
    const [loading, setLoading] = useState(true)

    let {
        id,
        name,
        user_id,
        cover_image,
        genres,
        modes,
        release_date,
        system_requirements,
        achievements,
        rating,
        players,
        related_games,
        auto_related_games,
        language,
        summary,
        description,
        trailer,
        additional_images,
        is_liked
    } = store.singleGame





    async function handleRelation() {

        let relatedGame1 = await actions.multiQueryGame(auto_related_games[0])
        let relatedGame2 = await actions.multiQueryGame(auto_related_games[1])
        let relatedGame3 = await actions.multiQueryGame(auto_related_games[2])
        // setAutoRelatedGames([relatedGame1, relatedGame2, relatedGame3])
        Promise.all([relatedGame1, relatedGame2, relatedGame3]).then((response) => {
            setAutoRelatedGames(response)
            setLoading(false)
        })
    }
    function handleRate({ target }) {
        setReview({
            ...review,
            [target.name]: target.value,
            ["game_id"]: id
        })
        console.log(review)

    }

    async function handleReviewSubmit() {
        let response = await actions.addReview(review)
        if (response == 200) {
            actions.getAllReviews(id)
        }
    }

    async function handleLike() {
        let updateResponse = await actions.updateLike(id)
        if (updateResponse == 200) {
            alert("Updated succesfully")
            actions.getGame(theid)
            console.log(store.singleGame)
        }
        let response = await actions.addLike(id)
        if (response == 200) {
            alert("Liked succesfully")
            actions.getGame(theid)
        }

    }

    async function handleAddToCart() {
        try {
            const response = await actions.addToCart(theid);
            if (response.success) {
                setSuccessMessage("Game added to cart successfully!");
                setErrorMessage(null);
            } else {
                setErrorMessage(response.message);
                setSuccessMessage(null);
            }
        } catch (error) {
            setErrorMessage("An error occurred while adding to cart.");
            setSuccessMessage(null);
        }
    }

    useEffect(() => {
        if (!user_id) return
        actions.getUser(user_id)
        actions.getAllReviews(id)
        console.log(store.reviews.totalRating)

    }, [user_id])


    useEffect(() => {
        actions.getGame(theid)
    }, [])

    useEffect(() => {
        if (Object.keys(store.singleGame).length == 0) return
        handleRelation()

    }, [auto_related_games])
    return (
        <>
            {
                loading ?
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    :
                    <div className="container">
                        <div className="row">
                            <div className="d-flex justify-content-center">
                                <div>
                                    <h1 className="d-flex justify-content-center">{name}</h1>
                                    <span>{genres}</span>
                                </div>
                            </div>
                            <div></div>
                            <div className="d-flex justify-content-center">
                                <img src={cover_image} className="w-25" />
                            </div>
                            <div className="d-flex justify-content-between">
                                <p>A game by {store.singleUser.name}</p>
                                <button className={is_liked ? "btn btn-danger" : "btn btn-primary"} onClick={() => handleLike()}>Like</button>
                            </div>
                            <div className="d-flex justify-content-center mt-2">
                                <iframe className="trailer" width="560" height="415" src={`https://www.youtube.com/embed/${trailer}`} title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
                            </div>
                            <div className="col-6 d-flex justify-content-center">
                                <p>{summary}</p>
                                <h2>Rating: {store.totalRating}</h2>                                
                            </div>
                            <div className="col-6 d-flex justify-content-center">
                                <div>
                                    <p>Game modes: {modes?.split(',').join(', ')}</p>
                                    <p>Release date: {release_date}</p>
                                    <p>PEGI: {rating}</p>
                                    <p>Number of players: {players}</p>
                                    <p>Achievements: {achievements}</p>
                                    <p>Language: {language}</p>
                                </div>
                            </div>
                            <div className="d-flex justify-content-center">
                                <h1 onClick={() => handleRelation()}>Related Games</h1>
                            </div>

                            {
                                autoRelatedGames &&
                                <div className="d-flex gap-3 justify-content-center">
                                    <div>
                                        <img src={autoRelatedGames[0].cover.url}></img>
                                        <p>{autoRelatedGames[0].name}</p>
                                    </div>
                                    <div>
                                        <img src={autoRelatedGames[1].cover.url}></img>
                                        <p>{autoRelatedGames[1].name}</p>
                                    </div>
                                    <div>
                                        <img src={autoRelatedGames[2].cover.url}></img>
                                        <p>{autoRelatedGames[2].name}</p>
                                    </div>
                                </div>
                            }
                            <div className="d-flex justify-content-center">
                                {system_requirements}
                            </div>
                            {additional_images && additional_images.length > 0 && (
                                <div className="additional-images mt-4">
                                    <h2>Additional Images</h2>
                                    <div className="d-flex flex-wrap justify-content-center">
                                        {additional_images.map((image, index) => (
                                            <img
                                                key={index}
                                                src={image}
                                                alt={`Additional image ${index + 1}`}
                                                className="m-2 hover-zoom"
                                                style={{ width: "150px", height: "100px", objectFit: "cover" }}
                                            />
                                        ))}
                                    </div>
                                </div>
                            )}
                                <div className="d-flex justify-content-center mt-3">
                                    <button className="btn btn-primary" onClick={handleAddToCart}>Add to Cart</button>
                                </div>
                                {errorMessage && (
                                    <div className="alert alert-danger mt-3 text-center">{errorMessage}</div>
                                )}
                                {successMessage && (
                                    <div className="alert alert-success mt-3 text-center">{successMessage}</div>
                                )}
                            <div>
                                <h1>Rate this game</h1>
                                <form className=""></form>
                                <div onChange={handleRate} className="btn-group" role="group" aria-label="Basic radio toggle button group">
                                    <input type="radio" className="btn-check" value="1" name="rating" id="btnradio1" autocomplete="off" />
                                    <label className="btn btn-outline-primary" htmlFor="btnradio1">1</label>
                                    <input type="radio" className="btn-check" value="2" name="rating" id="btnradio2" autocomplete="off" />
                                    <label className="btn btn-outline-primary" htmlFor="btnradio2">2</label>
                                    <input type="radio" className="btn-check" value="3" name="rating" id="btnradio3" autocomplete="off" />
                                    <label className="btn btn-outline-primary" htmlFor="btnradio3">3</label>
                                    <input type="radio" className="btn-check" value="4" name="rating" id="btnradio4" autocomplete="off" />
                                    <label className="btn btn-outline-primary" htmlFor="btnradio4">4</label>
                                    <input type="radio" className="btn-check" value="5" name="rating" id="btnradio5" autocomplete="off" />
                                    <label className="btn btn-outline-primary" htmlFor="btnradio5">5</label>
                                    <input type="radio" className="btn-check" value="6" name="rating" id="btnradio6" autocomplete="off" />
                                    <label className="btn btn-outline-primary" htmlFor="btnradio6">6</label>
                                    <input type="radio" className="btn-check" value="7" name="rating" id="btnradio7" autocomplete="off" />
                                    <label className="btn btn-outline-primary" htmlFor="btnradio7">7</label>
                                    <input type="radio" className="btn-check" value="8" name="rating" id="btnradio8" autocomplete="off" />
                                    <label className="btn btn-outline-primary" htmlFor="btnradio8">8</label>
                                    <input type="radio" className="btn-check" value="9" name="rating" id="btnradio9" autocomplete="off" />
                                    <label className="btn btn-outline-primary" htmlFor="btnradio9">9</label>
                                    <input type="radio" className="btn-check" value="10" name="rating" id="btnradio10" autocomplete="off" />
                                    <label className="btn btn-outline-primary" htmlFor="btnradio10">10</label>
                                </div>
                                
                                <input className="form-control" placeholder="Add a review..." name="review" onChange={handleRate}></input>
                                
                                <input type="submit" value="Submit" onClick={handleReviewSubmit} />
                            </div>
                        </div>
                        <div>
                            <h1>Reviews</h1>
                            {
                                store.reviews.map((item) => {
                                    return (
                                        <>
                                        {/* <h1>{userName}</h1> */}
                                            <h1>{item.user.name}</h1>
                                            <h2>{item.rating}</h2>
                                            <div>{item.review}</div>
                                        </>
                                    )
                                })
                            }
                        </div>
                    </div>
            }
        </>
    )
}