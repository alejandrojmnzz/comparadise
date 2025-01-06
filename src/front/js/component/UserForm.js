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
;

// Form data
return (

  <form onSubmit={handleSubmit} encType="multipart/form-data">
      {/* First Section */}
      <div>
        <label>Game Name:</label>
        <input 
        type="text"
        name="gameName" 
        value={formData.gameName} 
        onChange={handleChange} 
        required />
      </div>

      <div>
        <label>Image:</label>
        <input type="file" name="image" accept="image/*" onChange={handleChange} required />
      </div>

      {/* Second Section */}
      <div>
        <label>Genre:</label>
        <select name="genre" value={formData.genre} onChange={handleChange} required>
          <option value="">Select a genre</option>
          <option value="Action (shooter)">Action (shooter)</option>
          <option value="Action-adventure">Action-adventure</option>
          <option value="Adventure">Adventure</option>
          <option value="Casual">Casual</option>
          <option value="Puzzle">Puzzle</option>
          <option value="Role-playing">Role-playing</option>
          <option value="Simulation (sports, racing)">Simulation (sports, racing)</option>
          <option value="Strategy">Strategy</option>
        </select>
      </div>

      <div>
        <label>Game Modes:</label>
        <select name="modes" value={formData.modes} onChange={handleChange} required>
          <option value="">Select a mode</option>
          <option value="Campaign">Campaign</option>
          <option value="Capture the flag">Capture the flag</option>
          <option value="Deathmatch">Deathmatch</option>
          <option value="Oleada">Oleada</option>
          <option value="Multiplayer">Multiplayer</option>
        </select>
      </div>

      <div>
        <label>Release Date:</label>
        <input type="date" name="releaseDate" value={formData.releaseDate} onChange={handleChange} required />
      </div>

      {/* Third Section */}
      <div>
        <label>System Requirements:</label>
        <textarea name="systemRequirements" value={formData.systemRequirements} onChange={handleChange} required />
      </div>

      <div>
        <label>Achievements:</label>
        <input type="text" name="achievements" value={formData.achievements} onChange={handleChange} />
      </div>

      <div>
        <label>Media (Images or Videos):</label>
        <input type="file" name="media" accept="image/*,video/*" onChange={handleChange} />
      </div>

      <div>
        <label>Rating:</label>
        <select name="rating" value={formData.rating} onChange={handleChange} required>
          <option value="">Select a rating</option>
          <option value="G">G</option>
          <option value="PG">PG</option>
          <option value="PG-13">PG-13</option>
          <option value="R">R</option>
        </select>
      </div>
      </form>
)