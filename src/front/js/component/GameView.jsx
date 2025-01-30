import React, {useEffect, useContext, useState} from "react";
import { useParams } from "react-router-dom";
import { Context } from "../store/appContext";

export function GameView() {
    const {theid}= useParams()
    const {store, actions} = useContext(Context)
    const [autoRelatedGames, setAutoRelatedGames] = useState()

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
        auto_related_games,
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

    async function handleRelation() {
        let relatedGame1 = await actions.multiQueryGame(auto_related_games[0])
        let relatedGame2 = await actions.multiQueryGame(auto_related_games[1])
        let relatedGame3 = await actions.multiQueryGame(auto_related_games[2])
        setAutoRelatedGames([relatedGame1, relatedGame2, relatedGame3])
    }

        
    function getUser() {

        return store.singleUser
    }
    return(
        <>
        {console.log(autoRelatedGames)}

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
                        <h1  onClick={handleRelation}>Related Games</h1>
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
            </div>
        </div>
        </>
    )
}