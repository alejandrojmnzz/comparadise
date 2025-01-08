import React, {useState, useContext} from "react";

const GameForm = () => {
    const [formData, setFormData] = useState({
        gameName: "",
        image: null,
        genre: "",
        modes: "",
        releaseDate: "",
        systemRequirements: "",
        achievements: "",
        media: "",
        rating: "",
        players: "",
        relatedGames: "",
        language: "",
    });

// input changes
const handleChange = (e) => {
    const { name, value, files } = e.target;
    setFormData({
      ...formData,
      [name]: files ? files[0] : value,
    });
  };

  
  const handleSubmit = async (e) => {
    e.preventDefault();
    const formDataToSend = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      formDataToSend.append(key, value);
    });

    try {
      const response = await fetch("http://localhost:5000/api/games", {
        method: "POST",
        body: formDataToSend,
      });

      if (response.ok) {
        const data = await response.json();
        alert("Game successfully added!");
      } else {
        console.error(await response.text());
        alert("Error adding game.");
      }
    } catch (error) {
      console.error(error);
      alert("Network error.");
    }
  };

//form info
return (
    <form onSubmit={handleSubmit} encType="multipart/form-data">
      {/* First Section */}
      <div>
        <label>Game Name:</label>
        <input 
        type="text"
        name="gameName"
        value={formData.gameName} 
        onChange={handleChange} required 
        />
      </div>

      <div>
        <label>Image:</label>
        <input 
        type="file" 
        name="image" 
        accept="image/*" 
        onChange={handleChange} 
        required 
        />
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

      <div>
        <label>Number of Players:</label>
        <select name="players" value={formData.players} onChange={handleChange} required>
          <option value="">Select number of players</option>
          {[1, 2, 3, 4].map((num) => (
            <option key={num} value={num}>
              {num}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label>Related Games:</label>
        <input type="text" name="relatedGames" value={formData.relatedGames} onChange={handleChange} />
      </div>

      <div>
        <label>Languages:</label>
        <select name="language" value={formData.language} onChange={handleChange} required>
          <option value="">Select a language</option>
          <option value="Spanish">Spanish</option>
          <option value="English">English</option>
          <option value="French">French</option>
          <option value="Japanese">Japanese</option>
          <option value="Mandarin">Mandarin</option>
        </select>
      </div>

      <button type="submit">Submit</button>
    </form>
  );
};
export default GameForm