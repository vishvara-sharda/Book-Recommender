import React from 'react'
import "./Hero.css"
import Lottie from 'lottie-react'
import hero from "../graphic/hero.json"

function Hero() {
  return (
    <div style={{width:"100%", backgroundColor:"#061231"}}>
    <div className='hero-section container-lg'>
      <div className='row justify-content-center'>
        <div className='col-xs-11 col-sm 12 col-md-6 hero-left '>
          <div className='hero-content'>
            <h1>Discover Your Next Adventure </h1>
            <h5>Introducing our innovative Book Recommendation System – your personalized gateway to a world of captivating stories. Uncover literary gems tailored to your tastes and preferences, making every read a thrilling journey. Embark on a reading experience like never before</h5>
          </div>
        </div>
        <div className='col-xs-11 col-sm 12 col-md-6 hero-right'>
        <div className='hero-img'>
          <Lottie animationData={hero}/>
          {/* <img className='heroImg img-fluid ' src={require("../../images/hero.png")} alt='hero' /> */}
        </div>
        </div>
      </div>
    </div>
    </div>
  )
}

export default Hero
