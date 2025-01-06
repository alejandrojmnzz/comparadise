import React, { useContext } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";

export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<div>
			{/* {
				store.games.map((item) => {
					return (
						<h1>{item.name}</h1>
					)
				})
			} */}
		</div>
	);
};
