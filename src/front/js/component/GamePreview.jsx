import React from "react"
import { useContext } from "react"
import { Context } from "../store/appContext"
import { useState } from "react"

export function GamePreview() {
    const {store, actions} = useContext(Context)

    return(
        <div className="container">
            <div className="row game-preview-row justify-content-between mt-3">
                {
				store.recentGames.map((item) => {
					return (
						<div className="game-preview col-2 border rounded">
                            {
                                // item.
                            }
                        </div>
					)
				})
			    }
               
                
                <div className="game-preview col-2 border rounded">
                    aaa
                </div>
                <div className="game-preview col-2 border rounded">
                    aaa
                </div>
                <div className="game-preview col-2 border rounded">
                    aaa
                </div>
                <div className="game-preview col-2 border rounded">
                    aaa
                </div>
            </div>
        </div>
    )
}