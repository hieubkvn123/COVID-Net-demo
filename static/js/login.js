let get_default_headers = () => {
	return {
		'Content-Type' : 'application/json'
	}
}

$(document).ready(() => {
	$("#login_button").click((e) => {
		e.preventDefault()
		
		// Get login credentials
		let username = $("#username").val()
		let password = $("#password").val()
		let payload = {
			username : username,
			password : password
		}

		let headers = get_default_headers()

		// Send the data to the API
		axios.post("/login", payload, headers)
		.then(response => {
			// Get token from response and store
			console.log(response)
		}).catch(err => console.log(err))
	})
})
