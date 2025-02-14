import React from "react";
import {useState, useContext} from "react";
import {Context} from "../store/appContext"
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { NavLink } from "react-router-dom";
import { toast, ToastContainer, Flip } from "react-toastify";
import "react-toastify/dist/ReactToastify.css"
import "../../styles/reg-log.css"

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
            toast.error("All credentials are required ❌")
        }
        else {
            const response = await actions.login(user)
            if (response == 200 && store.token != null) {
                toast.success("Logged in successfully! 🎉")
                setTimeout(() => navigate("/"), 2000);
            }
            if (response == 404) {
                toast.error("Incorrect credentials 😖")
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
        <div>
            <button className="btn btn-secondary mt-2 go-back-button" onClick={() => navigate(-1)}>
                <i class="fa-solid fa-rotate-left"></i>
                    &nbsp; Go Back</button>
            <ToastContainer
                position="top-center"
                autoClose={2000}
                hideProgressBar={false}
                newestOnTop
                closeOnClick={false}
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
                theme="dark"
                transition={Flip}
            />
        
            <div className="container justify-content-center align-items-center col-4 pt-5">
                <h1 className="text-center">Login</h1>
            <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label htmlFor="exampleInputEmail1" className="form-label">Email address</label>
                        <input name="email" type="email" onChange={handleChange} className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="exampleInputPassword1" className="form-label">Password</label>
                        <input name="password" type="password" onChange={handleChange} className="form-control" id="exampleInputPassword1" />
                    </div>
                    <button type="submit" className="btn btn-primary mb-2 align-items-center">Submit</button>
                </form>
                <div className="aling-items-center">
                <NavLink to="/register">You don't have an account?</NavLink>
                </div>
        </div>
        </div>
    )
}