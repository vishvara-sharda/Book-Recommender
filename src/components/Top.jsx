import React, { useState } from 'react'
import "./Top.css";
import Book from './Book';
import { useEffect } from 'react';

function Top(props) {
  const [BookData, setBookData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        // Replace 'API_ENDPOINT' with your actual API URL
        const response = await fetch('http://127.0.0.1:5001/api/top_books');

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const jsonData = await response.json();
        const BookData = jsonData.data;
        console.log(BookData)
        setBookData(BookData);
        setLoading(false);
      } catch (err) {
        setError(err);
        setLoading(false);
      }
    }
    fetchData();
  }, []);


  return (
    <div className='top-section container'>
      {props.page === 'search' ? <h2>Search result</h2> :
        <h1>Top Books</h1>
      }
      <div className='top-books-section'>
        <div className='row'>
          {
            // Check if BookData is defined and loading is false
            BookData && !loading && BookData.map((book, index) => (
              <Book name={book['Book-Title']} by={book['Book-Author']} img={book['Image-URL-M']} key={index} />
            ))
          }

        </div>
      </div>
    </div>
  )
}

export default Top
