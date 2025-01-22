const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			token: localStorage.getItem("token") || null,
			recentGames: [],
			singleGame: {},
			singleUser: {}
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
			}
		}
	};
};

export default getState;
