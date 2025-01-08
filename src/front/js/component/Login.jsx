import React from "react";
import {useState, useContext} from "react";
import {Context} from "../store/appContext"
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { NavLink } from "react-router-dom";

export function Login() {

    const {store, actions} = useContext(Context)
    const navigate = useNavigate()
    const [user, setUser] = useState({
        email: "",
        password: ""
    })
    
    function handleChange({target}) {
        setUser({
            ...user,
            [target.name]: target.value
        })
    }

    async function handleSubmit(event) {
        event.preventDefault()

        if (user.email.trim() == "" || user.password == "") {
            alert("All credentials are required")
        }
        else {
            const response = await actions.login(user)
            if (response == 200 && store.token != null) {
                alert("Logged")
                navigate("/")
            }
            if (response == 404) {
                alert("Incorrect credentials")
            }
            console.log(response)
        }
    }
    useEffect(() => {
        if (store.token != null) {
            navigate('/')
        }
    }, [])
    return (
        <div className="container">
            <form onSubmit={handleSubmit}>
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
                <NavLink to="/register">You don't have an account?</NavLink>
        </div>
    )
}