import React, { useContext, useEffect, useState } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import "../../styles/api-search.css";
import { GamePreview } from "../component/GamePreview.jsx";
import { FeaturedGames } from "../component/FeaturedGames.jsx";
import { useNavigate } from "react-router-dom";
import "../../styles/index.css"

export const Home = () => {
	const { store, actions } = useContext(Context);
	const [query, setQuery] = useState("")
	const [suggestions, setSuggestions] = useState([])
	const [selectedGame, setSelectedGame] = useState()
	const [relatedGames, setRelatedGames] = useState()
	const navigate = useNavigate()


	function handleChange({ target }) {
		setQuery(target.value)

	}

	async function handleEnter(event) {
		if (event.keyCode == 13 && query.trim() != "") {
			let result = await actions.searchAPIGame(query)
			setSuggestions(result)
		}
	}

	async function handleClick(item) {

		setSuggestions([])
		setQuery("")
		let gameResponse = await actions.multiQueryGame(item.id)
		setSelectedGame(gameResponse)
		console.log(gameResponse)
		let comparation = await actions.compareAPIAndGame(gameResponse)
		// console.log(list(comparation[0].values()[0]['total']))
		let relatedGame = await actions.getGame(Object.values(comparation[0])[0]["id"])
		let relatedGame2 = await actions.getGame(Object.values(comparation[1])[0]["id"])
		let relatedGame3 = await actions.getGame(Object.values(comparation[2])[0]["id"])

		setRelatedGames([relatedGame, relatedGame2, relatedGame3])
	}


	return (
		<>
			<FeaturedGames />

			<div className="container api-searchbar">
				<div className="d-flex justify-content-center">
					<h4>Looking for a certain adventure?</h4>
				</div>

				<div className="d-flex justify-content-center">
					<div className="d-flex w-75 search-api">
						<i className="fa-solid fa-magnifying-glass icon-api-search"></i>
						<input type="search" value={query} className="input-api-search w-100" onChange={handleChange} onKeyDown={handleEnter} placeholder="Search for a game to compare" />


						<ul className="api-suggestions-list">

							{
								suggestions.map((item) => {
									if (query != "") {
										return (
											<li key={item.id} onClick={() => handleClick(item)}>
												{item.name}
											</li>
										)
									}
									else {
										setSuggestions([])
									}
								})
							}
						</ul>


					</div>
				</div>
			</div>

			{
				selectedGame &&
				relatedGames &&
				<div className="container api-game-comparation mt-2">

					<div>
						<div className="d-flex align-items-center">
							<img src={`https://images.igdb.com/igdb/image/upload/t_1080p/${selectedGame.cover.url.split("/")[7]}`} className="w-25 px-2 rounded" />
							<h4 className="d-flex justify-content-center mx-3">Similar
								<br></br>
								Games:
							</h4>
							<div className="d-flex justify-content-between gap-3 mx-3 align-items-center w-100">

								<div className="comparation-image-container">
									<img src={relatedGames[0].cover_image} className="comparation-image rounded" onClick={() => navigate(`/game/${relatedGames[0].id}`)}></img>
								</div>
								<div className="comparation-image-container">
									<img src={relatedGames[1].cover_image} className="comparation-image rounded" onClick={() => navigate(`/game/${relatedGames[0].id}`)}></img>
								</div>
								<div className="comparation-image-container">
									<img src={relatedGames[2].cover_image} className="comparation-image rounded" onClick={() => navigate(`/game/${relatedGames[0].id}`)}></img>
								</div>

							</div>
						</div>

					</div>





				</div>


			}



			<GamePreview />

		</>
	);
};