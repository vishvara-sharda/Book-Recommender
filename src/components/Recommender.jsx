import React, { useState } from 'react'
import "./Recommender.css"
// import hero2 from "../graphic/hero2.json"
import Lottie from 'lottie-react'
import hero3 from "../graphic/hero3.json"
import hero2 from "../graphic/hero22.json"
import Search from './SearchSection'


function Recommender() {
    const [BookTitle, setBookTitle] = useState("");
    const [SearchBookTitle, setSearchBookTitle] = useState("");

    const handleChange = () => {
        const SearchBookTitle = BookTitle
        setSearchBookTitle(SearchBookTitle)
        console.log("hello", SearchBookTitle)
    }

    return (
        <div >
            <div className='recommender-section'>
                <div className='container'>
                    <h1 className='book-rec'>Unleash Your Next Chapter</h1>
                    <hr />
                    <div className='row' >
                        <div className='col-md-6 left'>
                            <div className='input-container'>
                                <input
                                    type='text'
                                    placeholder='Search by Book, author, ISBN'
                                    value={BookTitle}
                                    onChange={e => setBookTitle(e.target.value)}
                                />
                                <button className='btn search-btn'
                                    onClick={() => handleChange()}
                                >Search</button>
                                <div className='book-anime'>
                                    <Lottie animationData={hero3} />
                                </div>
                            </div>

                        </div>
                        <div className='col-md-6 right'>
                            <div>
                                <img src={require("../images/WhatsApp_Image_2023-08-16_at_3.16.39_PM-removebg-preview.png")} alt='anime2' />
                                {/* <Lottie animationData={hero2} /> */}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <Search title={SearchBookTitle} />
        </div>
    )
}

export default Recommender
