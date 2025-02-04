import React, {useEffect, useContext, useState} from "react";
import { useParams } from "react-router-dom";
import { Context } from "../store/appContext";

export function GameView() {
    const {theid}= useParams()
    const {store, actions} = useContext(Context);
    const [errorMessage, setErrorMessage] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);
    let {name,
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
        language, 
        summary, 
        description, 
        trailer,
        additional_images
    } = store.singleGame


    useEffect(() => {
        actions.getGame(theid)
    }, [])

    useEffect(() => {
        if(!user_id) return
        actions.getUser(user_id)
    }, [user_id])

    function getUser() {

        return store.singleUser
    }
    async function handleAddToCart() {
        
        const response = await actions.addToCart(theid);
        if (!response.success) {
            setErrorMessage(response.message);
            setSuccessMessage(null);
        } else {
            setSuccessMessage(response.message);
            setErrorMessage(null);
        }
    } 
    return(
        <>
        <div className="container">
            <div className="row">
                <div className="d-flex justify-content-center">
                    <div>
                        <h1 className="d-flex justify-content-center">{name}</h1>  
                        <span>{genres}</span>  
                    </div>            
                </div>
                <div className="d-flex justify-content-center">
                     <img src={cover_image} className="w-25"/>
                </div>
                <div>
                    <p>A game by {store.singleUser.name}</p>
                </div>
                <div className="d-flex justify-content-center mt-2">
                    <iframe className="trailer" width="560" height="415" src={`https://www.youtube.com/embed/${trailer}`} title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
                </div>
                <div className="col-6 d-flex justify-content-center">
                    <p>{summary}</p>
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
                    <div>
                        <h1>Related Games</h1>
                        <p className="d-flex justify-content-center">{related_games}</p>
                    </div>
                </div>
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
                        <div className="alert alert-danger mt-3 text-center"> {errorMessage}</div>
                    )}
                    {successMessage && (
                        <div className="alert alert-success mt-3 text-center">{successMessage}</div>
                    )}
            </div>
        </div>
        </>
    )
}