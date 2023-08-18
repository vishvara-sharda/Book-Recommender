import React, { useState } from 'react'
import "./Navbar.css"
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';
import { useNavigate } from 'react-router-dom';
import Lottie from 'lottie-react'
import logo from "../graphic/logo.json"

function Navbar(props) {

  const [navbar, setNavbar] = useState(false);
   const navigate = useNavigate();

  const toggleNavbar = () => {
    // console.log("clicked")
    setNavbar(!navbar);
  }

  const sendToRecommend = () => {
    navigate("/");
  }



  return (
    <nav >
       <div style={{width:"70px"}}>
          <Lottie animationData={logo} />
       </div>
      {/* <img id='logo' onClick={sendToHome} className='logo-img img-fluid img-responsive' src={require("../../images/codeify.png")} alt='logo' /> */}
      <div className='hamburger'>
        {navbar ? <CloseIcon style={{fill:"#fff", fontSize:"200%"}} onClick={toggleNavbar} /> : <MenuIcon   style={{fill:"#fff", fontSize:"200%"}} onClick={toggleNavbar} />}
      </div>
      <ul id="nav-bar" className={navbar ? 'active' : 'act'} >
       <li>
          <p>Home</p>
        </li>
        <li>
          <p onClick={sendToRecommend}>Recommendation</p>
        </li>
        {/* <li>
          <button className='talk-btn btn'>Let's talk</button>
        </li> */}
      </ul>
    </nav>
  )
}

export default Navbar
