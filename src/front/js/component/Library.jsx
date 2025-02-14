    import React, { useContext, useEffect } from "react";
    import { Context } from "../store/appContext";
    import { useNavigate } from "react-router-dom";

    export function Library() {
        const {store, actions} = useContext(Context);
        const navigate = useNavigate();

        useEffect(() => {
            actions.fetchLibrary();
        }, []);

        console.log("Updated Library Data:", store.library);

        return (
            <div>
                <h1 className="text-center">Your Library</h1>
                <button className="btn btn-secondary mt-2 go-back-button" onClick={() => navigate(-1)}>
                    <i class="fa-solid fa-rotate-left"></i>
                    &nbsp; Go Back</button>
                    <div className="row">
                        {store.library.map((item, index) => (
                            <div key={index} className="d-flex justify-content-center gap-3 col-md-4 mb-3">
                                <div className="card gap-3">
                                    <img 
                                    src={item.cover_image} 
                                    className="card-img-top" 
                                    alt={item.name}
                                    onClick={() => navigate(`/game/${item.id}`)}
                                    />
                                    <div className="card-body" >
                                        <h5 className="card-title">{item.name}</h5>
                                        <p className="card-text">{item.summary}</p>
                                        <a href={item.game_file} download={`${item.name}`} target="_blank">Download</a>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                {/* )} */}
            </div>
        )
    }