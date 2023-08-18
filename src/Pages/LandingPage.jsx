import React from 'react'
import Navbar from '../components/Navbar'
import Hero from '../components/Hero'
import Top from '../components/Top'
import RecommendPage from './RecommendPage'
import Recommender from '../components/Recommender'
import Footer from '../components/Footer'
import Search from '../components/SearchSection'

function LandingPage() {
  return (
    <div>
       <Navbar />
      <Hero />
      <Top />
      <Recommender />
      
      <Footer />
    </div>
  )
}

export default LandingPage
