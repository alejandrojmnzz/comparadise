import React from "react"
import { useState, useContext } from "react"
import Context from "../store/appContext"

export function Register() {
    const { actions } = useContext(Context)
    const [user, setUser] = useState({
        name: "",
        email: "",
        password: ""
    })

    function handleChange({ target }) {
        setUser({
            ...user,
            [target.name]: target.value
        })
        if (response == 200) {
            alert("User created")
            if (response == 400) {
                alert("User already exists")
            }
        }
        async function handleSubmit(event) {
            const response = await actions.register(user)
        }
        return (
            <div className="container">
                <div>
                    <div className="mb-3">
                        <label for="name" className="form-label">Name</label>
                        <input name="name" type="text" onChange={handleChange} className="form-control" id="name" />
                    </div>
                    <div className="mb-3">
                        <label for="exampleInputEmail1" className="form-label">Email address</label>
                        <input name="email" type="email" onChange={handleChange} className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" />
                    </div>
                    <div className="mb-3">
                        <label for="exampleInputPassword1" className="form-label">Password</label>
                        <input name="password" type="password" onChange={handleChange} className="form-control" id="exampleInputPassword1" />
                    </div>
                    <button type="submit" className="btn btn-primary" onClick={handleSubmit}>Submit</button>
                </div>
            </div>
        )
    }
}