import React from "react"
import { useState, useContext } from "react"
import { Context } from "../store/appContext"
import { NavLink } from "react-router-dom"
import { useNavigate } from "react-router-dom"

export function Register() {
    const { actions } = useContext(Context)
    const navigate = useNavigate()
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
    }
    async function handleSubmit(event) {
        event.preventDefault()
        if (user.name.trim() == "" || user.email.trim() == "" || user.password == "") {
            alert("All credentials are required")
        }
        else {
            const response = await actions.register(user)
            if (response == 201) {
                alert("User created")
                navigate("/login")
            }
            if (response == 409) {
                alert("User already exists")
            }
            if (response == 400) {
                alert("Error registering")
            }
        }
    }
    return (
        <div className="container">
            <form onSubmit={handleSubmit}>
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
                <button type="submit" className="btn btn-primary mb-2">Submit</button>
            </form>
            <NavLink to="/login">Already have an account?</NavLink>
        </div>
    )
}