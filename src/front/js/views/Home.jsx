import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import "../../styles/api-search.css";
import { GamePreview } from "../component/GamePreview.jsx";

export const Home = () => {
	const { store, actions } = useContext(Context);
	return (
		<>
		<div>
			<div className="d-flex justify-content-center">
				<input 
				className="api-search form-control"
				type="search"
				/>
			</div>
			<GamePreview/>
			
		</div>
		</>
	);
};
