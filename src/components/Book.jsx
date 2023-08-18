import React from 'react'
import "./Book.css"

function Book(props) {
  return (
    <div className='book-div col-xs-4 col-sm-3 col-md-3 col-lg-2'>
    <div className='card book'>
        <img src={props.img} alt='book' />
        <h3>{props.name}</h3>
        <h4>{props.by}</h4>
    </div>
    </div>
  )
}

export default Book
