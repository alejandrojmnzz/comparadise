import React, { useCallback, useContext, useEffect } from "react";
import { Context } from "../store/appContext";

export function Library() {
    const {store, actions} = useContext(Context);

    useEffect(() => {
        actions.fetchLibrary();
    }, []);

    return (
        <div>
            <h1 className="text-center">Your Library</h1>
            {store.library.length === 0 ? (
                <p className="text-center">No games purchased yet.</p>
            ) : (
                <div className="row">
                    {store.library.map((item, index) => (
                        <div key={index} className="col-md-4 mb-3">
                            <div className="card">
                                <img src={item.game.cover_image} className="card-img-top" alt={item.game.name}/>
                                <div className="card-body">
                                    <h5 className="card-title">{item.game.name}</h5>
                                    <p className="card-text">{item.game.summary}</p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}