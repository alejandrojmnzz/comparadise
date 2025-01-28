import React, {useState, useContext, useEffect} from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";
import { array } from "prop-types";



export const GameForm = () => {

const {store, actions} = useContext(Context)
const navigate = useNavigate()

  useEffect(() => {
    if (store.token == null) {
      navigate('/register')
    }
  }, [])

  const [formData, setFormData] = useState({
      name: "",
      genres: [],
      cover_image:"",
      // additional_images: "",
      modes: [],
      player_perspective: [],
      themes: [],
      keywords: "",
      release_date: "",
      system_requirements: "",
      achievements: "",
      rating: "",
      players: "",
      related_games: "",
      language: "",
      summary: "",
      description: "",
      trailer: ""
  });
  // const [coverImage, setCoverImage] = useState(null);
  // const [mediaFiles, setMediaFiles] = useState([]);

  const handleChange = (event) => {
      const { name, value } = event.target;
      setFormData({ ...formData, [name]: value });
  };

  const handleCheckboxes = ({target}) => {
    const {name, value, checked} = target
    if (checked == true) {
      setFormData({...formData, [name]: [
        ...formData[name],
        value
      ]})
    }
    else {
      let filteredData = formData[name].filter((item) => item != value)
      setFormData({...formData, [name]: filteredData})
      console.log(formData)
    }
  }

  const handleSubmit = async (event) => {
      try {
      event.preventDefault();
      const formDataObj = new FormData()
      formDataObj.append("cover_image", formData.cover_image);
      formDataObj.append("trailer", formData.trailer.split('=')[1])
      formDataObj.append("modes", formData.modes.join())
      formDataObj.append("genres", formData.genres.join())
      formDataObj.append("player_perspective", formData.player_perspective.join())
      formDataObj.append("themes", formData.themes.join())

      Object.keys(formData).forEach(key => formDataObj.append(key, formData[key]));
        alert("Game successfully added")
      
      // if (formData.additional_images) {
      //     Array.from(formData.additional_images).forEach((file, index) => {
      //       console.log(formData.additional_images);
      //       formDataObj.append(`additional_images[${index}]`, file);
      //     });
      // }


      
        console.log(formDataObj)
        const response = await fetch(process.env.BACKEND_URL+"/submit-game", {
          method: "POST",
          body: formDataObj,
          headers: {
            "Authorization": `Bearer ${store.token}`
          }
      });
      const result = await response.json();
      } catch (error) {
        console.log(error)
        return false
      }
      
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
        <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#collapseGenres" aria-expanded="false" aria-controls="collapseExample">
          Select a genre
        </button>
        <div class="collapse" id="collapseGenres">
        <div class="card card-body w-25">
          <ul class="list-group" onChange={handleCheckboxes}>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Point-and-click" id="Point-and-click"/>
                <label class="form-check-label stretched-link" for="Point-and-click">Point-and-click</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Fighting" id="Fighting"/>
                <label class="form-check-label stretched-link" for="Fighting">Fighting</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Shooter" id="Shooter"/>
                <label class="form-check-label stretched-link" for="Shooter">Shooter</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Music" id="Music"/>
                <label class="form-check-label stretched-link" for="Music">Music</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Platform" id="Platform"/>
                <label class="form-check-label stretched-link" for="Platform">Platform</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Puzzle" id="Puzzle"/>
                <label class="form-check-label stretched-link" for="Puzzle">Puzzle</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Racing" id="Racing"/>
                <label class="form-check-label stretched-link" for="Racing">Racing</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Real Time Strategy (RTS)" id="Real Time Strategy (RTS)"/>
                <label class="form-check-label stretched-link" for="Real Time Strategy (RTS)">Real Time Strategy (RTS)</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="modgenreses" type="checkbox" value="Role-playing (RPG)" id="Role-playing (RPG)"/>
                <label class="form-check-label stretched-link" for="Role-playing (RPG)">Role-playing (RPG)</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Simulator" id="Simulator"/>
                <label class="form-check-label stretched-link" for="Simulator">Simulator</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Sport" id="Sport"/>
                <label class="form-check-label stretched-link" for="Sport">Sport</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Strategy" id="Strategy"/>
                <label class="form-check-label stretched-link" for="Strategy">Strategy</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Turn-based strategy (TBS)" id="Turn-based strategy (TBS)"/>
                <label class="form-check-label stretched-link" for="Turn-based strategy (TBS)">Turn-based strategy (TBS)</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Tactical" id="Tactical"/>
                <label class="form-check-label stretched-link" for="Tactical">Tactical</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Hack and slash/Beat 'em up" id="Hack and slash/Beat 'em up"/>
                <label class="form-check-label stretched-link" for="Hack and slash/Beat 'em up">Hack and slash/Beat 'em up</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Quiz/Trivia" id="Quiz/Trivia"/>
                <label class="form-check-label stretched-link" for="Quiz/Trivia">Quiz/Trivia</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Pinball" id="Pinball"/>
                <label class="form-check-label stretched-link" for="Pinball">Pinball</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Arcade" id="Arcade"/>
                <label class="form-check-label stretched-link" for="Arcade">Arcade</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Visual Novel" id="Visual Novel"/>
                <label class="form-check-label stretched-link" for="Visual Novel">Visual Novel</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="Card & Board Game" id="Card & Board Game"/>
                <label class="form-check-label stretched-link" for="Card & Board Game">Card & Board Game</label>
              </li>
              <li class="list-group-item">
                <input class="form-check-input me-1" name="genres" type="checkbox" value="MOBA" id="MOBA"/>
                <label class="form-check-label stretched-link" for="MOBA">MOBA</label>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div>
        <label>Game Modes:</label>
        <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#collapseModes" aria-expanded="false" aria-controls="collapseExample">
          Select a mode
        </button>
      <div class="collapse" id="collapseModes">
        <div class="card card-body w-25">
        <ul class="list-group" onChange={handleCheckboxes}>
            <li class="list-group-item">
              <input class="form-check-input me-1" name="modes" type="checkbox" value="Single Player" id="Single Player"/>
              <label class="form-check-label stretched-link" for="Single Player">Single Player</label>
            </li>
            <li class="list-group-item">
              <input class="form-check-input me-1" name="modes" type="checkbox" value="Multiplayer" id="Multiplayer"/>
              <label class="form-check-label stretched-link" for="Multiplayer">Multiplayer</label>
            </li>
            <li class="list-group-item">
              <input class="form-check-input me-1" name="modes" type="checkbox" value="Co-operative" id="Co-operative"/>
              <label class="form-check-label stretched-link" for="Co-operative">Co-operative</label>
            </li>
            <li class="list-group-item">
              <input class="form-check-input me-1" name="modes" type="checkbox" value="Split screen" id="Split screen"/>
              <label class="form-check-label stretched-link" for="Split screen">Split screen</label>
            </li>
            <li class="list-group-item">
              <input class="form-check-input me-1" name="modes" type="checkbox" value="Massively Multiplayer Online (MMO)" id="Massively Multiplayer Online (MMO)"/>
              <label class="form-check-label stretched-link" for="Massively Multiplayer Online (MMO)">Massively Multiplayer Online (MMO)</label>
            </li>
            <li class="list-group-item">
              <input class="form-check-input me-1" name="modes" type="checkbox" value="Battle Royale" id="Battle Royale"/>
              <label class="form-check-label stretched-link" for="Battle Royale">Battle Royale</label>
            </li>
          </ul>
        </div>
      </div>
      </div>

      <div>
        <label>Player Perspective:</label>
          <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#collapsePerspective" aria-expanded="false" aria-controls="collapseExample">
              Select a player perspective
          </button>
          <div class="collapse" id="collapsePerspective">
            <div class="card card-body w-25">
            <ul class="list-group" onChange={handleCheckboxes}>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="player_perspective" type="checkbox" value="First person" id="First person"/>
                  <label class="form-check-label stretched-link" for="First person">First person</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="player_perspective" type="checkbox" value="Third person" id="Third person"/>
                  <label class="form-check-label stretched-link" for="Third person">Third person</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="player_perspective" type="checkbox" value="Bird view / Isometric" id="Bird view / Isometric"/>
                  <label class="form-check-label stretched-link" for="Bird view / Isometric">Bird view / Isometric</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="player_perspective" type="checkbox" value="Side view" id="Side view"/>
                  <label class="form-check-label stretched-link" for="Side view">Side view</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="player_perspective" type="checkbox" value="Text" id="Text"/>
                  <label class="form-check-label stretched-link" for="Text">Text</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="player_perspective" type="checkbox" value="Auditory" id="Auditory"/>
                  <label class="form-check-label stretched-link" for="Auditory">Auditory</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="player_perspective" type="checkbox" value="Virtual Reality" id="Virtual Reality"/>
                  <label class="form-check-label stretched-link" for="Virtual Reality">Virtual Reality</label>
                </li>
              </ul>
            </div>
          </div>
      </div>

      <div>
        <label>Themes:</label>
        <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThemes" aria-expanded="false" aria-controls="collapseExample">
          Select a theme
        </button>
          <div class="collapse" id="collapseThemes">
            <div class="card card-body w-25">
            <ul class="list-group" onChange={handleCheckboxes}>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Non-fiction" id="Non-fiction"/>
                  <label class="form-check-label stretched-link" for="Non-fiction">Non-fiction</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Sandbox" id="Sandbox"/>
                  <label class="form-check-label stretched-link" for="Sandbox">Sandbox</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Educational" id="Educational"/>
                  <label class="form-check-label stretched-link" for="Educational">Educational</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Open world" id="Open world"/>
                  <label class="form-check-label stretched-link" for="Open world">Open world</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Warfare" id="Warfare"/>
                  <label class="form-check-label stretched-link" for="Warfare">Warfare</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Party" id="Party"/>
                  <label class="form-check-label stretched-link" for="Party">Party</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="4X (explore, expand, exploit, and exterminate)" id="4X (explore, expand, exploit, and exterminate)"/>
                  <label class="form-check-label stretched-link" for="4X (explore, expand, exploit, and exterminate)">4X (explore, expand, exploit, and exterminate)</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Mystery" id="Mystery"/>
                  <label class="form-check-label stretched-link" for="Mystery">Mystery</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Action" id="Action"/>
                  <label class="form-check-label stretched-link" for="Action">Action</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Fantasy" id="Fantasy"/>
                  <label class="form-check-label stretched-link" for="Fantasy">Fantasy</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Science fiction" id="Science fiction"/>
                  <label class="form-check-label stretched-link" for="Science fiction">Science fiction</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Horror" id="Horror"/>
                  <label class="form-check-label stretched-link" for="Horror">Horror</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Thriller" id="Thriller"/>
                  <label class="form-check-label stretched-link" for="Thriller">Thriller</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Survival" id="Survival"/>
                  <label class="form-check-label stretched-link" for="Survival">Survival</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Historical" id="Historical"/>
                  <label class="form-check-label stretched-link" for="Historical">Historical</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Stealth" id="Stealth"/>
                  <label class="form-check-label stretched-link" for="Stealth">Stealth</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Comedy" id="Comedy"/>
                  <label class="form-check-label stretched-link" for="Comedy">Comedy</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Business" id="Business"/>
                  <label class="form-check-label stretched-link" for="Business">Business</label>
                </li>
                <li class="list-group-item">
                  <input class="form-check-input me-1" name="themes" type="checkbox" value="Romance" id="Romance"/>
                  <label class="form-check-label stretched-link" for="Romance">Romance</label>
                </li>
              </ul>
            </div>
          </div>
      <div>
        <label>
            Keywords/Tags:
            <input 
            type="text"
            name="keywords" 
            value={formData.keywords} 
            onChange={handleChange} 
            required />
          </label>
      </div>

       
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
{/* 
      <div>
        <label>Additional Images:</label>
        <input
        type="file" 
        name="additional_images" 
        multiple 
        onChange={(event) => {
          setFormData({ ...formData, additional_images: event.target.files });
        }}
        />
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

      <div>
        <label>Summary:</label>
        <input type="text" name="summary" value={formData.summary} onChange={handleChange} />
      </div>

      <div>
        <label>Description:</label>
        <input type="text" name="description" value={formData.description} onChange={handleChange} />
      </div>

      <div>
        <label>Trailer (Link del navegador de YouTube)</label>
        <input type="text" name="trailer" value={formData.trailer} onChange={handleChange} />
      </div>

      <button type="submit">Submit</button>
    </form>
  );
};
export default GameForm