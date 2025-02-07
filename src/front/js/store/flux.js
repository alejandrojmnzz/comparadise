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
			currentUserGames: null,
			userGames: null,
			reviews: [],
			userReviewName: [],
			featuredGames: null
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
					console.log(error)
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
				} catch (error) {
					console.log(error)
				}
			},
			getLocalUser: async (id) => {
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
					setStore({...getStore().userReviewName,
						"name": data.name})
					return(data)
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
					return data[0].result[0]
				} catch (error) {
					console.log(error)
				}
			},
			compareAPIAndGame: async (game) => {
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
				return data
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
					return response.status
				}
				catch (error) {
					console.log(error)
				}
			},
			getAllReviews: async (id) => {
				let response = await fetch(`${process.env.BACKEND_URL}/get-all-reviews/${id}`,
					{
						method: 'GET'
					}
				)
				let data = await response.json()
				let review = 0
				for (let item of data) {
					review = review + item.rating
				}

				setStore({reviews: data,
					totalRating: (review / data.length)
				})
				return data
			},
			addLike: async (id) => {
				let response = await fetch(`${process.env.BACKEND_URL}/like-game/${id}`,
					{
					method: 'GET',
					
					headers: {
						'Authorization': `Bearer ${getStore().token}`
					}
				}
				)
				return response.status
			},
			updateLike: async (id) => {
				let response = await fetch(`${process.env.BACKEND_URL}/update-like/${id}`,
					{
						method: 'GET',
						headers: {
						'Authorization': `Bearer ${getStore().token}`
						}
					}
				)
				return response.status
			},
			getFeaturedGames: async () => {
				let response = await fetch(`${process.env.BACKEND_URL}/get-game-likes`,
					{
						method: 'GET'
					}
				)
				let data = await response.json()
				setStore({featuredGames: [data[0], data[1], data[2], data[3], data[4]]})
				return data
			}
		}
	};
};


export default getState;
