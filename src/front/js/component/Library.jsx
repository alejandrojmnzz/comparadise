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
            {/* {store.library.length === 0 ? (
                <p className="text-center">No games purchased yet.</p>
            ) : ( */}
                <div className="row">
                    {store.library.map((item, index) => (
                        <div key={index} className="col-md-4 mb-3">
                            <div className="card">
                                <img 
                                src={item.cover_image} 
                                className="card-img-top" 
                                alt={item.name}
                                onClick={() => navigate(`/game/${item.id}`)}
                                />
                                <div className="card-body" >
                                    <h5 className="card-title">{item.name}</h5>
                                    <p className="card-text">{item.summary}</p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            {/* )} */}
        </div>
    )
}