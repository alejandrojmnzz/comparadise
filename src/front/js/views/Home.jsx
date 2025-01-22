import React, { useContext, useEffect, useState } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import { GamePreview } from "../component/GamePreview.jsx";
import "../../styles/index.css"

export const Home = () => {
	const { store, actions } = useContext(Context);
	const [query, setQuery] = useState("")
	const [suggestions, setSuggestions] = useState([])
	function handleChange({target}) {
		setQuery(target.value)
		console.log(query)
	}

	async function handleEnter(event) {
		if (event.keyCode == 13 && query.trim() != "" ) {
			let result = await actions.searchAPIGame(query)
			setSuggestions(result)
		}
	}

	return (
		<>
		<div className="h-100 align-items-end">
			<div className="d-flex justify-content-center">
				<input type="search" value={query} className="form-control w-50" onChange={handleChange} onKeyDown={handleEnter}/>
			</div>
			<div className="d-flex justify-content-center">
				
				<ul className="suggestions-list w-50">
					{
						suggestions.map((item) => {
							return (
								<li key={item.id} className="">
									{item.name}
								</li>
							)
						}) 
					}
				</ul>
			</div>
			<GamePreview/>
			
		</div>
		</>
	);
};