import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";

import { Context } from "../store/appContext";

export const Login = () => {
    const { store, actions } = useContext(Context);

    return (
        <div className="container">
           <h1>Bienvenido al area privada!!!</h1>
        </div>
    );
};
