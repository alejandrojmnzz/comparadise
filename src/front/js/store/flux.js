const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			token: localStorage.getItem("token") || null,
			recentGames: [],
			singleGame: {},
			singleUser: {},
			searchResults: [],
			isLoading: false,
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
			get_game: async (id) => {
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
				} catch (error) {
					console.log(error)
				}
			},
			get_user: async (id) => {
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
					const response = await response.fetch(`${process.env.BACKEND_URL}/games-search?query=${query}`);

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
			}
		}
	};
};

export default getState;
