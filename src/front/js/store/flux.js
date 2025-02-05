import { library } from "webpack";

const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			token: localStorage.getItem("token") || null,
			recentGames: [],
			singleGame: {},
			singleUser: {},
			searchResults: [],
			isLoading: false,
			relatedGames: [],
			cart: [],
			currentUserGames: null,
			userGames: null,
			library:[],
			reviews: []
		},
		actions: {
			register: async (user) => {
				try {
					let response = await fetch(`${process.env.BACKEND_URL}/register`,
						{
						method: 'POST',
						headers: {
							"Content-Type": "application/json"
						},
						body: JSON.stringify(user)
						}
					)

					return response.status
				}
				catch (error) {
					console.log(error.args)
					return false
					
				}
			},
			login: async (user) => {
				try {
				let response = await fetch(`${process.env.BACKEND_URL}/login`,
					{
						method: 'POST',
						headers: {
							"Content-Type": "application/json"
						},
						body: JSON.stringify(user)
					})
				let data = await response.json()
				if (response.ok) {
					setStore({
						token: data.token
					})
					localStorage.setItem("token", data.token)
				}
				return response.status
				}
				catch (error) {
					return false
				}
			},
			logout: () => {
				setStore({token: null})
			},
			recentGames: async () => {
				try {
					let response = await fetch(`${process.env.BACKEND_URL}/get-recent-games`,
						{
							method: "GET"
						}
					)
					let data = await response.json()
					
					setStore({
						recentGames: data
					})
				
				}
				catch (error) {
					return false
				}
			},
			getGame: async (id) => {
				try {
					let response = await fetch(`${process.env.BACKEND_URL}/get-game`,
						{
						method: 'POST',
						headers: {
							"Content-Type": "application/json"
						},
						body: JSON.stringify(id)
					}
					)
					let data = await response.json()
					setStore({
						singleGame: data
					})
					console.log(data)
					return data
				} catch (error) {
					console.log(error)
				}
			},
			getUser: async (id) => {
				try {
					let response = await fetch(`${process.env.BACKEND_URL}/get-user`,
						{
						method: 'POST',
						headers: {
							"Content-Type": "application/json"
						},
						body: JSON.stringify(id)
					}
					)
					let data = await response.json()
					setStore({
						singleUser: data
					})
					console.log(data)
				} catch (error) {
					console.log(error)
				}
			},
			fetchSearchResults: async (query) => {
				setStore({isLoading: true});

				try{
					const response = await fetch(`${process.env.BACKEND_URL}/games-search?query=${query}`);

					if (response.ok){
						const data = await response.json();
						setStore({searchResults: data});
					} else {
						console.error("No search results found.");
						setStore({searchResults: []});
					}
				} catch (error) {
					console.error("Error fetching search results", error);
					setStore({searchResults: []});
				} finally {
					setStore({isLoading: false});
				}
			},
			searchAPIGame: async (query) => {
				try {
					let response = await fetch(`${process.env.BACKEND_URL}/get-api-games`,
						{
							method: 'POST',
							headers: {
								'Content-Type': 'application/json'
							},
							body: JSON.stringify(query)
						}
					)
					let data = await response.json()
					console.log(data)
					return data
				} catch (error) {
					console.log(error)	
					return false
				}
			},
			getAPIImage: async (id) => {
				try {
					let response = await fetch(`${process.env.BACKEND_URL}/get-api-image`,
						{
							method: 'POST',
							headers: {
								'Content-Type': 'application/json'
							},
							body: JSON.stringify(id)
						}
					)
					let data = await response.json()
					return data
				} catch (error) {
					console.log(error)
				}
			},
			multiQueryGame: async (id) => {
				try {
					let response = await fetch(`${process.env.BACKEND_URL}/multiquery-game`,
						{
							method: 'POST',
							headers: {
								'Content-Type': 'application/json'
							},
							body: JSON.stringify(id)
						}
					)
					let data = await response.json()
					console.log(data)
					return data[0].result[0]
				} catch (error) {
					console.log(error)
				}
			},
			compareAPIAndGame: async (game) => {
				console.log(game)
				let response = await fetch(`${process.env.BACKEND_URL}/compare-api-and-game`,
					{
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(game)
					}
				)
				let data = await response.json()
				console.log(data)
				return data
			},
			fetchCart: async (userId) => {
				try{
					let response = await fetch(`${process.env.BACKEND_URL}/cart`, {
						method:"GET",
						headers: {
							"Content-Type": "application/json",
                			"Authorization": `Bearer ${getStore().token}`
						}
					});
					let data = await response.json();
					setStore({cart: data});
				} catch (error) {
					console.error("Error fetching cart:", error);
					setStore({ cart: []});
				}
			},
			addToCart: async (gameId) => {
				try {
					let response = await fetch(`${process.env.BACKEND_URL}/add-to-cart`, {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
							"Authorization": `Bearer ${getStore().token}`
						},
						body: JSON.stringify({ game_id: gameId })
					});
			
					let data = await response.json();
			
					if (!response.ok) {
						return { success: false, message: data.message || "Failed to add to cart." };
					}
					getActions().fetchCart();
			
					return { success: true, message: "Game added to cart!" };
				} catch (error) {
					console.error("Error adding to cart:", error);
					return { success: false, message: "An error occurred." };
				}
			},
			removeFromCart: async (cartId) => {
				try {
					let response = await fetch(`${process.env.BACKEND_URL}/remove-from-cart/${cartId}`, {
						method: "DELETE",
						headers: {
							"Authorization": `Bearer ${getStore().token}`
						}
					});
			
					if (response.ok) {
						// Refresh the cart state
						getActions().fetchCart();
						return { success: true, message: "Game removed from cart!" };
					} else {
						return { success: false, message: "Failed to remove game from cart." };
					}
				} catch (error) {
					console.error("Error removing from cart:", error);
					return { success: false, message: "An error occurred." };
				}
			},
			fetchLibrary: async () => {
				try {
					let response = await fetch(`${process.env.BACKEND_URL}/library`, {
						method: "GET",
						headers: {"Authorization": `Bearer ${getStore().token}`}
					});
					let data = await response.json();
					setStore({library: data});
				} catch (error) {
					console.log(error);
				}
			},
			purchaseGames: async () => {
				try {
					let response = await fetch(`${process.env.BACKEND_URL}/purchase`, {
						method: "POST",
						headers: {"Authorization": `Bearer ${getStore().token}`}
					});
					return await response.json();
				} catch (error) {
					console.log(error);
					return {success: false};
				}
			},
			compareGameAndAPI: async (game) => {
				let response = await fetch(`${process.env.BACKEND_URL}/compare-game-and-api`,
					{
						method: 'POST',
						headers: {
							'Content-Type': 'application/json'
						},
						body: JSON.stringify(game)
					}
				)
				let data = await response.json()
				console.log(game)
				return data
			},
			getCurrentUserGames: async () => {
				try {
				let response = await fetch(`${process.env.BACKEND_URL}/my-games`,
					{
						method: 'GET',
						headers: {
							'Content-Type': 'application/json',
							'Authorization': `Bearer ${getStore().token}`
						}
					}
				)
				let data = await response.json()
				setStore({currentUserGames: data})
				console.log(data)
				return data
			}
			catch (error) {
				console.log(error)
			}
			},
			getUserGames: async (user_id) => {
				try {
				let response = await fetch(`${process.env.BACKEND_URL}/user-games`,
					{
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
						},
						body: JSON.stringify(user_id)
					}
				)
				let data = await response.json()
				setStore({userGames: data})
				console.log(data)
				return data
			}
			catch (error) {
				console.log(error)
			}
			},
			addReview: async (review) => {
				try {
					let response = await fetch(`${process.env.BACKEND_URL}/add-review`,
						{
							method: 'POST',
							headers: {
								'Content-Type': 'application/json',
								'Authorization': `Bearer ${getStore().token}`
							},
							body: JSON.stringify(review)
						}
					)
					let data = await response.json()
					console.log(data)
					return data
				}
				catch (error) {
					console.log(error)
				}
			},
			getAllReviews: async () => {
				let response = await fetch(`${process.nextTick.BACKEND_URL}/get-all-reviews`,
					{
						method: 'GET'
					}
				)
				let data = await response.json()
				console.log(data)
				setStore({reviews: data})
				return data
			}
		}
	};
}


export default getState
