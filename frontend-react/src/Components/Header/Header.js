import "./Header.css";
import { Link } from 'react-router-dom'; // Import Link from react-router-dom if using React Router for navigation
// Import the Train component from the Train.js file
import logo from 'C:/Users/Prasida/Documents/CICG_V1/UI_cicg_v1/src/CICG_guls2.jpg'

export default function Header({ title, train, test }){
    return(
        <div className="header">
          <Link to="/">
          <div className="header-logo"><img src={logo} alt="Logo" width={250} height={70}/></div>
          </Link>
           
            <div className="header-title">{title}</div>
            <div className="train-test">
            
            <Link to="/train"> {/* Set the 'to' attribute to the URL of the 'Train' page */}
          <div>
          
      {train}</div>
      </Link>
        <Link to="/test"> {/* Set the 'to' attribute to the URL of the 'Test' page */}
          <div className="test-space">{test}</div>
        </Link>
            </div>
            
        </div>
    );
}

