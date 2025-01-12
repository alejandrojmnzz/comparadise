import React, {useState, useContext} from "react";

export const GameForm = () => {
  const [formData, setFormData] = useState({
      name: "",
      genre: "",
      cover_image:"",
      modes: "",
      release_date: "",
      system_requirements: "",
      achievements: "",
      rating: "",
      players: "",
      related_games: "",
      language: ""
  });
  // const [coverImage, setCoverImage] = useState(null);
  // const [mediaFiles, setMediaFiles] = useState([]);

  const handleChange = (event) => {
      const { name, value } = event.target;
      setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (event) => {
      event.preventDefault();
      const formDataObj = new FormData()
      formDataObj.append("cover_image", formData.cover_image);
      Object.keys(formData).forEach(key => formDataObj.append(key, formData[key]));
      
        alert("Game successfully added")
      

      console.log(formDataObj)
      const response = await fetch(process.env.BACKEND_URL+"/submit-game", {
          method: "POST",
          body: JSON.stringify(formDataObj),
      });

      const result = await response.json();
      console.log(result);
  };

//form info
return (
    <form onSubmit={handleSubmit}>
      <label>
        Game Name:
        <input 
        type="text"
        name="name" 
        value={formData.name} 
        onChange={handleChange} 
        required />
      </label>

      <label>
        Cover Image:
        <input 
        type="file" 
        name="cover_image" 
        onChange={(event) => {
          setFormData({...formData, cover_image: event.target.files[0] })
        }}  
        />
      </label>

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
          <option value="Multiplayer">Multiplayer</option>
        </select>
      </div>

      <div>
        <label>Release Date:</label>
        <input type="date" name="release_date" value={formData.release_date} onChange={handleChange} required />
      </div>

      {/* Third Section */}
      <div>
        <label>System Requirements:</label>
        <textarea name="system_requirements" value={formData.system_requirements} onChange={handleChange} required />
      </div>

      <div>
        <label>Achievements:</label>
        <input type="text" name="achievements" value={formData.achievements} onChange={handleChange} />
      </div>

      {/* <div>
        <label>Media:</label>
        <input type="file" name="media" accept="image/*,video/*" onChange={handleChange} />
      </div> */}

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
        <input type="text" name="related_games" value={formData.relatedGames} onChange={handleChange} />
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