import React, { useState } from 'react'

// function UserForm() {
//     const [formData, setFormData] = useState({ name: '', email: ''});
//     const [error, setError] = useState ('');

//     const handleChange = (event) => {
//         const { name, value } = event.target;
//         setFormData ({ ...formData , [name]: value });
//     };

//     const handleSubmit = async (event) => {
//         event.preventDefault();
//         if (!formData.name || !formData.email) {
//             setError('Llenar todos los campos obligatorios');
//             return;
//         }
//         setError('')
//     }
// Datos enviados al backend
    // try {
    //     const response = await fetch()
    // }
};

// Datos formulario

return (
    <div>
        <h1>Formulario Añadir Videojuego</h1>
        <form onSubmit={handleSubmit}>
            <div>
                <label>Nombre del juego:</label>
                <input
                type = "text"
                name = "name"
                value = {FormData.name}
                onChange={handleChange}
                />
            </div>

            <div>
                <label>Nombre del juego:</label>
                <input
                type = "text"
                name = "name"
                value = {FormData.name}
                onChange={handleChange}
                />
            </div>

            <div>
                <label>Nombre del juego:</label>
                <input
                type = "text"
                name = "name"
                value = {FormData.name}
                onChange={handleChange}
                />
            </div>

            <div>
                <label>Nombre del juego:</label>
                <input
                type = "text"
                name = "name"
                value = {FormData.name}
                onChange={handleChange}
                />
            </div>

            <div>
                <label>Nombre del juego:</label>
                <input
                type = "text"
                name = "name"
                value = {FormData.name}
                onChange={handleChange}
                />
            </div>

            <div>
                <label>Nombre del juego:</label>
                <input
                type = "text"
                name = "name"
                value = {FormData.name}
                onChange={handleChange}
                />
            </div>

            <div>
                <label>Nombre del juego:</label>
                <input
                type = "text"
                name = "name"
                value = {FormData.name}
                onChange={handleChange}
                />
            </div>

            <div>
                <label>Nombre del juego:</label>
                <input
                type = "text"
                name = "name"
                value = {FormData.name}
                onChange={handleChange}
                />
            </div>
        </form>
    </div>
)