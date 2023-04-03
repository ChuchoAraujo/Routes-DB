import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import { useEffect } from "react/cjs/react.production.min";

export const Home = () => {
	const { store, actions } = useContext(Context);
	const navigate = useNavigate();

	const [name, setName] = useState("");
	const [last_name, setLastName] = useState("");
	const [age, setAge] = useState("");
	const [nameLogin, setNameLogin] = useState("");
	const [last_nameLogin, setLastNameLogin] = useState("");
	const [ageLogin, setAgeLogin] = useState("");
	const [signupMessage, setSignupMessage] = useState("");

	// ---------------------------- POST / SIGNUP----------------------------------//

	const signup = () => {
		fetch(process.env.BACKEND_URL + "/api/signup", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				"name": name,
				"last_name": last_name,
				"age": age
			}),
		})
			.then((response) => response.json())
			.then((result) => {
				console.log(result);
				setSignupMessage("¡Te has registrado exitosamente!");
			})
			.catch((error) => console.log("error", error));
	};

// ---------------------------- POST / LOGIN----------------------------------//
	const login = () => {

		fetch(process.env.BACKEND_URL + "/api/login", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},

			body: JSON.stringify({
				"name": nameLogin,
				"last_name": last_nameLogin,
				"age": ageLogin
			}),
		})
			.then((response) => response.json())
			.then((result) => {
				if (result.token) {
					localStorage.setItem("token", result.token);
					navigate("/login");
				} else {
					setError(result.msg);
				}
				console.log(result.msg)
			})
			.catch((error) => console.log("error", error));
	};

	// ---------------------------- GET / MEMBERS----------------------------------//

	const getMembers = () => {
		fetch(process.env.BACKEND_URL + "/api/members", {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Authorization: "Bearer " + localStorage.getItem("token"),
			},
		})
			.then((response) => response.json())
			.then((result) => {
				console.log(result)
				setSignupMessage("¡Te has registrado exitosamente!");
			})
			.catch((error) => console.log("error", error));
	}
	


	return (
		<>
			<div className="container text-center mt-5 d-flex justify-content-center">

				<div className="card col-6 p-5">
					<h1 className="m-4">Sign Up</h1>
					<div className="m-2">
						<label htmlFor="nombre">Nombre</label>
						<input type="text" value={name} onChange={(e)=> setName(e.target.value)} id="nombre" placeholder="Escribe tu nombre"></input>
					</div>
					<div className="m-2">
						<label htmlFor="last_name">Last name</label>
						<input type="text" value={last_name} onChange={(e) => setLastName(e.target.value)} id="last_name" placeholder="Escribe tu nombre"></input>
					</div>
					<div className="m-2">
						<label htmlFor="age">Age</label>
						<input type="text" value={age} onChange={(e) => setAge(e.target.value)} id="age" placeholder="Escribe tu nombre"></input>
					</div>
					<button className="btn btn-warning m-3" onClick={signup}>Enviar</button>
					{signupMessage && <div className="alert alert-success" role="alert">{signupMessage}</div>}
					
				</div> 


				<div className="card col-6 p-5">
					<h1 className="m-4">Login</h1>
					<div className="m-2">
						<label htmlFor="nombre">Nombre</label>
						<input type="text" value={nameLogin} onChange={(e) => setNameLogin(e.target.value)} id="nombre" placeholder="Escribe tu nombre"></input>
					</div>
					<div className="m-2">
						<label htmlFor="last_name">Last name</label>
						<input type="text" value={last_nameLogin} onChange={(e) => setLastNameLogin(e.target.value)} id="last_name" placeholder="Escribe tu nombre"></input>
					</div>
					<div className="m-2">
						<label htmlFor="age">Age</label>
						<input type="text" value={ageLogin} onChange={(e) => setAgeLogin(e.target.value)} id="age" placeholder="Escribe tu nombre"></input>
					</div>
					<button className="btn btn-warning m-3" onClick={login}>Enviar</button>
					

				</div>

			</div>

			<div className="row text-center mt-3">
				<div className="col-4"></div>
				<div className="col-4">
					<h2 >Ver todos los members</h2>
					<button className="btn btn-success p-2 m-3" onClick={getMembers}>ver members</button>
				</div>
				<div className="col-4"></div>
			</div>
		</>

	);
};
