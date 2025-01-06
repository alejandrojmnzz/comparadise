const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
		},
		actions: {
			register: async (user) => {
				try {
					let response = await fetch(`${process.env.BACKEND_URL}/api/register`,
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
					return false
				}
			}
		}
	};
};

export default getState;
