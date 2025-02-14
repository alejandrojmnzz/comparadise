import React, { useEffect, useContext, useState } from "react";
import { NavLink, useNavigate, useParams, useRoutes } from "react-router-dom";
import { Context } from "../store/appContext";
import '../../styles/game-view.css'
import { toast, ToastContainer, Flip } from "react-toastify";
import "react-toastify/dist/ReactToastify.css"

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
    const [errorMessage, setErrorMessage] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);
    const [image, setImage] = useState()
    const navigate = useNavigate()

    let {
        id,
        name,
        user_id,
        cover_image,
        genres,
        modes,
        player_perspective,
        themes,
        release_date,
        system_requirements,
        achievements,
        pegi,
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

    const [liked, setLiked] = useState(is_liked)


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

    }

    async function handleReviewSubmit() {
        let response = await actions.addReview(review)
        if (store.token == null) {
            toast.error("You must be logged ❌")
        }
        if (response == 200) {
            toast.success("Review submitted! ✔️")

            actions.getAllReviews(id)
        }
    }

    async function handleLike() {
        try {
            setLiked(!liked)
            let updateResponse = await actions.updateLike(id)
            if (updateResponse == 200) {
                actions.getGame(theid)
            }
            let response = await actions.addLike(id)
            if (response == 200) {
                actions.getGame(theid)
            }
        }
        catch (error) {
            console.log(error)
        }
    }

    async function handleAddToCart() {
        try {
            const response = await actions.addToCart(theid);
            if (response.success) {
                toast.success("Game added to cart successfully!");
            } else {
                toast.error(response.message);
            }
        } catch (error) {
            toast.error("An error occurred while adding to cart.");
        }
    }

    useEffect(() => {
        if (!user_id) return
        actions.getUser(user_id)
        actions.getAllReviews(id)
        setImage(additional_images[0])
    }, [user_id])


    useEffect(() => {
        actions.getGame(theid)
    }, [])

    useEffect(() => {
        if (Object.keys(store.singleGame).length == 0) return
        handleRelation()

    }, [auto_related_games])

    useEffect(() => {
        setLiked(is_liked)
    }, [is_liked])

    return (
        <>
            {
                loading ?

                    <div className="d-flex justify-content-center align-items-center">
                        <div className="spinner-border text-primary" role="status">
                            <span className="visually-hidden">Loading...</span>
                        </div>
                    </div>
                    :
                    <div className="container">
                        <button className="btn btn-secondary mt-2 go-back-button" onClick={() => navigate(-1)}>
                            <i class="fa-solid fa-rotate-left"></i>
                                &nbsp; Go Back</button>
                        <ToastContainer
                            position="top-center"
                            autoClose={2000}
                            hideProgressBar={false}
                            newestOnTop
                            closeOnClick={false}
                            rtl={false}
                            pauseOnFocusLoss
                            draggable
                            pauseOnHover
                            theme="dark"
                            transition={Flip}
                        />
                        <div className="row">
                            <div className="d-flex justify-content-center">

                                <h1 className="col-2 d-flex justify-content-center text-center game-title w-50">{name}</h1>
                            </div>
                            <div className="d-flex justify-content-center">
                                <p>{summary}</p>

                            </div>

                   
                            <div className="d-flex justify-content-center">
                                <div className="col-7 d-flex">
                                    <iframe className="trailer" height="425" src={`https://www.youtube.com/embed/${trailer}`} title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerPolicy="strict-origin-when-cross-origin" allowFullScreen></iframe>
                                    <div>
                                        <button className="like fs-2 text-danger" onClick={() => handleLike()}>{liked ? <i className={`${liked && "like-icon"} fa-solid fa-heart`}></i> : <i className="fa-regular fa-heart"></i>}</button>
                                    </div>
                                </div>
                                    
                            </div>
                          
                            
                            
                            <div className="d-flex justify-content-center">
                                <div className="d-flex justify-content-between col-7">
                                    <p>A game by <NavLink to={`/user-games/${store.singleUser.id}`}>{store.singleUser.name}</NavLink></p>
                                    
                                </div>
                            </div>
                            <div className="col-12 d-flex justify-content-center mb-3">
                                <h2>Rating: {store.totalRating}</h2>
                            </div>
                            <div className="d-flex justify-content-center">
                                <div className="col-9 d-flex justify-content-between gap-1">
                                    <div className="aspect d-flex flex-column align-items-center">
                                        <h5><b>Genres</b></h5>
                                        <ul className="w-100">
                                            {

                                                genres.split(",").map((item) => {
                                                    return (
                                                        <li className="m-0">{item}</li>
                                                    )
                                                })
                                            }
                                        </ul>
                                    </div>
                                    <div className="aspect d-flex flex-column align-items-center">
                                        <h5><b>Game Modes</b></h5>
                                        <ul className="w-100">
                                            {
                                                modes.split(",").map((item) => {
                                                    return (
                                                        <li className="m-0">{item}</li>
                                                    )
                                                })
                                            }
                                        </ul>

                                    </div>
                                    <div className="aspect d-flex flex-column align-items-center">
                                        <h5><b>Player Perspectives</b></h5>
                                        <ul className="w-100">
                                            {
                                                player_perspective.split(",").map((item) => {
                                                    return (
                                                        <li className="m-0">{item}</li>
                                                    )
                                                })
                                            }
                                        </ul>
                                    </div>
                                    <div className="aspect d-flex flex-column align-items-center">
                                        <h5><b>Themes</b></h5>
                                        <ul className="w-100">
                                            {
                                                themes.split(",").map((item) => {
                                                    return (
                                                        <li className="m-0">{item}</li>
                                                    )
                                                })
                                            }
                                        </ul>
                                    </div>
                                </div>
     
                            </div>
                            <div className="d-flex justify-content-center mt-1">
                                <div className="col-6 d-flex justify-content-between additional-info">
                                    <p ><b className="d-flex justify-content-center">Release date</b> {release_date}</p>
                                    <p><b className="d-flex justify-content-center">PEGI</b>{pegi}</p>
                                    <p><b className="d-flex justify-content-center">Number of players</b>{players}</p>
                                    <p><b className="d-flex justify-content-center">Language</b>{language}</p>
                                </div>
                            </div>
                            {additional_images && additional_images.length > 0 && (
                                <div className="additional-images mt-4">
                                    <div className="d-flex justify-content-center mt-2">
                                        <img src={image} className="additional-image" />
                                    </div>
                                    <div className="d-flex flex-wrap justify-content-center">
                                        {additional_images.map((item, index) => {

                                            // if (index == 0) {
                                            //     setImage(item)
                                            // }
                                            return (
                                                <img
                                                    key={index}
                                                    src={item}
                                                    alt={`Additional image ${index + 1}`}
                                                    className={`m-2 hover-zoom rounded ${item == image && "hover-add-images"}`}
                                                    style={{ width: "150px", height: "100px", objectFit: "cover", cursor: "pointer" }}
                                                    onClick={({ target }) => setImage(target.src)}
                                                />
                                            )
                                        })}
                                    </div>
                                </div>
                            )}
                            <div className="d-flex justify-content center">
                                <p>{description}</p>
                            </div>
                            <div className="d-flex justify-content-center mt-3">
                                <h1 onClick={() => handleRelation()}>Related Games</h1>
                            </div>

                            {
                                autoRelatedGames &&
                            <div className="d-flex justify-content-center">
                                <div className="row ">
                                    <div className="col-sm-5 col-xl-4">
                                        <img className="related-game-view" src={`https://images.igdb.com/igdb/image/upload/t_1080p/${autoRelatedGames[0].cover.url.split("/")[7]}`}></img>
                                        <p>{autoRelatedGames[0].name}</p>
                                    </div>
                                    <div className="col-sm-5 col-xl-4">
                                        <img className="related-game-view" src={`https://images.igdb.com/igdb/image/upload/t_1080p/${autoRelatedGames[1].cover.url.split("/")[7]}`}></img>

                                        <p>{autoRelatedGames[1].name}</p>
                                    </div>
                                    <div className="col-sm-5 col-xl-4">
                                    <img className="related-game-view" src={`https://images.igdb.com/igdb/image/upload/t_1080p/${autoRelatedGames[2].cover.url.split("/")[7]}`}></img>
                                        <p>{autoRelatedGames[2].name}</p>
                                    </div>
                                </div>
                                </div>
                            }
                            <div className="d-flex justify-content-center mt-3">
                            <h3>System Requirements</h3>
                            </div>
                            <div className="d-flex justify-content-center">
                                <p>{system_requirements}</p>
                            </div>

                            <div className="d-flex justify-content-center mt-3">
                                <button className="btn cart-button" onClick={handleAddToCart}>Add to Cart</button>
                            </div>
                            {errorMessage && (
                                <div className="alert alert-danger mt-3 text-center">{errorMessage}</div>
                            )}
                            {successMessage && (
                                <div className="alert alert-success mt-3 text-center">{successMessage}</div>
                            )}
                            <div>
                                <div className="d-flex justify-content-center mt-3">
                                    <h1>Rate this game</h1>
                                </div>
                                <div className="d-flex justify-content-center">
                                <div className="rate-game">
                                <div onChange={handleRate} className="btn-group btn-group-lg mb-2 d-flex justify-content-center" role="group" aria-label="Basic radio toggle button group">
                                    <input type="radio" className="btn-check" value="1" name="rating" id="btnradio1" autoComplete="off" />
                                    <label className="btn btn-outline-info" htmlFor="btnradio1">1</label>
                                    <input type="radio" className="btn-check" value="2" name="rating" id="btnradio2" autoComplete="off" />
                                    <label className="btn btn-outline-info" htmlFor="btnradio2">2</label>
                                    <input type="radio" className="btn-check" value="3" name="rating" id="btnradio3" autoComplete="off" />
                                    <label className="btn btn-outline-info" htmlFor="btnradio3">3</label>
                                    <input type="radio" className="btn-check" value="4" name="rating" id="btnradio4" autoComplete="off" />
                                    <label className="btn btn-outline-info" htmlFor="btnradio4">4</label>
                                    <input type="radio" className="btn-check" value="5" name="rating" id="btnradio5" autoComplete="off" />
                                    <label className="btn btn-outline-info" htmlFor="btnradio5">5</label>
                                    <input type="radio" className="btn-check" value="6" name="rating" id="btnradio6" autoComplete="off" />
                                    <label className="btn btn-outline-info" htmlFor="btnradio6">6</label>
                                    <input type="radio" className="btn-check" value="7" name="rating" id="btnradio7" autoComplete="off" />
                                    <label className="btn btn-outline-info" htmlFor="btnradio7">7</label>
                                    <input type="radio" className="btn-check" value="8" name="rating" id="btnradio8" autoComplete="off" />
                                    <label className="btn btn-outline-info" htmlFor="btnradio8">8</label>
                                    <input type="radio" className="btn-check" value="9" name="rating" id="btnradio9" autoComplete="off" />
                                    <label className="btn btn-outline-info" htmlFor="btnradio9">9</label>
                                    <input type="radio" className="btn-check" value="10" name="rating" id="btnradio10" autoComplete="off" />
                                    <label className="btn btn-outline-info" htmlFor="btnradio10">10</label>
                                </div>

                                <input className="form-control review-input" placeholder="Add a review..." name="review" onChange={handleRate}></input>
                            <div className="d-flex justify-content-end">
                                <input className="btn btn-primary mt-2" type="submit" value="Submit" onClick={handleReviewSubmit} />
                            </div>
                            </div>
                                </div>
                            </div>
                        </div>
                        <div className="row">
                            <h1>Reviews</h1>
                    
                            
                            {
                                store.reviews.map((item, index) => {
                                    return (
                                        <div key={index} className="pb-3  col-6">
                                            <div className="review-div" >
                                                <div className="rating-review">
                                                    <p className="m-0 fs-5">This user rated this game a <b>{item.rating}/10</b></p>
                                                </div>
                                            <div className="name-review">
                                                <h2><b>{item.user.name}</b> says:</h2>
                                                <div className="review-text">{item.review}</div>
                                            </div>
                                            </div>
                                        </div>
                                    )
                                })
                            }
                            </div>

                        </div>
              
            }
        </>
    )
}