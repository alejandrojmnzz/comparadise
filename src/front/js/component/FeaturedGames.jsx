import React from "react";
import '../../styles/featured.css'
import { useEffect } from "react";
import { Context } from "../store/appContext";
import { useContext } from "react"
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export function FeaturedGames() {
  const { store, actions } = useContext(Context)
  const [loading, setLoading] = useState(true)
  const [relatedGame, setRelatedGame] = useState([])
  const navigate = useNavigate()

  async function handleFeature() {
    let response = await actions.getFeaturedGames()
    for (let item of store.featuredGames) {
      if (item) {
        let comparation = await actions.multiQueryGame(item.game.auto_related_games[0])
        relatedGame.push(comparation)
      }
    }
    setLoading(false)

  }

  useEffect(() => {
    handleFeature()
  }, [])

  return (
    <>
      {

        loading ?
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          :
          store.featuredGames.map((item, index) => {

            return (
              <div key={index}>
                {
                  item &&
                  <div id="container" key={item.game.id} onClick={() => navigate(`/game/${item.game.id}`)}>
                    <div id="left">
                      <img src={item.game.cover_image} />
                    </div>
                    <div id="right">
                      <img src={`https://images.igdb.com/igdb/image/upload/t_1080p/${relatedGame[index].cover.url.split("/")[7]}`} />
                    </div>
                  </div>
                }
              </div>

            )

          })
      }
    </>
  )



}