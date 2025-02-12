import React from "react";
import '../../styles/featured.css'
import { useEffect, useContext, useState } from "react";
import { Context } from "../store/appContext";
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
        <div className="d-flex justify-content-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>

          :
          <div id="carouselExampleIndicators" className="carousel slide">
            <div className="carousel-indicators">

              {
                store.featuredGames.filter((item) => item != undefined).map((item, index) => {

                  return (
                    <button
                      type="button"
                      data-bs-target="#carouselExampleIndicators"
                      data-bs-slide-to={index}
                      className={index == 0 ? "active" : ""}

                      aria-current={index == 0 ? "true" : ""}
                      aria-label={`Slide ${Number(index) + 1}`}></button>
                  )
                })
              }

            </div>
            <div className="carousel-inner">
              {
                store.featuredGames.filter((item) => item != undefined).map((item, index) => {
                  return (
                    <div className={index == 0 ? "carousel-item active" : "carousel-item"}>
                      <div id="container" onClick={() => navigate(`/game/${item.game?.id}`)}>
                        <div id="left">
                          <img src={item?.game?.cover_image}/>
                            <div className="content">
                                <div className="name fs-1">{item.game.name}</div>
                                <div className="genres fs-5">{item.game.genres.split(',')[0]}{item.game.genres.split(',')[1] ? ", " : ""}{item.game.genres.split(',')[1]}{item.game.genres.split(',')[2] ? ", " : ""}{item.game.genres.split(',')[2]}</div>
                            </div>
                        </div>
    
                        <div id="right">
                          <img src={`https://images.igdb.com/igdb/image/upload/t_1080p/${relatedGame[index]?.cover?.url.split("/")[7]}`} />
                            <div className="content">
                            <div className="name fs-1">{relatedGame[index]?.name}</div>
                            <div className="genres fs-4">Rating: {Math.round(relatedGame[index]?.rating)}/100</div>
                            </div>
                        </div>
                      </div>
                    </div>
                  )
                })
              }
            </div>
            <button className="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
              <span className="carousel-control-prev-icon" aria-hidden="true"></span>
              <span className="visually-hidden">Previous</span>
            </button>
            <button className="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
              <span className="carousel-control-next-icon" aria-hidden="true"></span>
              <span className="visually-hidden">Next</span>
            </button>
          </div >
      }
    </>
  )
}