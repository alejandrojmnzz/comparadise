import React, { useContext } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import { GamePreview } from "../component/GamePreview.jsx";

export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<>
		<div className="h-100 align-items-end">
			

			<GamePreview/>
			
		</div>
		</>
	);
};
