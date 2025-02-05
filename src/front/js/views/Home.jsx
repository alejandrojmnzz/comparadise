import React, { useContext, useEffect, useState } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import "../../styles/api-search.css";
import { GamePreview } from "../component/GamePreview.jsx";
import { FeaturedGames } from "../component/FeaturedGames.jsx";
import "../../styles/index.css"

export const Home = () => {
	const { store, actions } = useContext(Context);
	const [query, setQuery] = useState("")
	const [suggestions, setSuggestions] = useState([])
	const [selectedGame, setSelectedGame] = useState()
	const [relatedGames, setRelatedGames] = useState()

	function handleChange({target}) {
		setQuery(target.value)

	}

	async function handleEnter(event) {
		if (event.keyCode == 13 && query.trim() != "" ) {
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
		<FeaturedGames/>
		<div className="h-100 align-items-end">
			<div className="d-flex justify-content-center">
				<input type="search" value={query} className="form-control w-50" onChange={handleChange} onKeyDown={handleEnter} placeholder="Search for a game to compare"/>
			</div>

			<div className="d-flex justify-content-center">
				<ul className="api-suggestions-list w-50">
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
			<div className="container d-flex">
				{
					selectedGame &&
					<>	
						<img src={`https://images.igdb.com/igdb/image/upload/t_1080p/${selectedGame.cover.url.split("/")[7]}`} className="w-25 px-2"/>
						<div className="d-flex justify-content-center align-items-center">
							<div className="ps-2">
								<p className="d-flex justify-content-center">Games similar to</p>
									<p><b>{selectedGame.name}</b>:</p>
							</div>
						</div>
					</>
				}
			</div>
			<div className="d-flex">
				{
					relatedGames &&
					<>
						<div> 
							<p>{relatedGames[0]["name"]}</p>
							<img src={relatedGames[0].cover_image} className="h-25"></img>
						</div>
						<div>
							<p>{relatedGames[1]["name"]}</p>
							<img src={relatedGames[1].cover_image} className="h-25"></img>
						</div>
						<div>
							<p>{relatedGames[2]["name"]}</p>
							<img src={relatedGames[2].cover_image} className="h-25"></img>
						</div>

					</>
				}
				
			
			</div>

			<GamePreview/>
			
		</div>
		</>
	);
};