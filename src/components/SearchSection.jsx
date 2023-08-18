import React, { useState } from 'react'
import "./Top.css";
import Book from './Book';
import { useEffect } from 'react';

function Search({title}) {
  const [BookData, setBookData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        // Replace 'API_ENDPOINT' with your actual API URL
        const response = await fetch('http://127.0.0.1:5001/api/recommend?book_title=' + title);

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const jsonData = await response.json();
        const BookData = jsonData;
        console.log(BookData)
        setBookData(BookData);
        setLoading(false);
      } catch (err) {
        setError(err);
        setLoading(false);
      }
    }
    fetchData();
  }, [title]);


  return (
    <div className='top-section container'>
        <h1>Books</h1>
      <div className='top-books-section'>
        <div className='row'>
          {
            // Check if BookData is defined and loading is false
            BookData && !loading && BookData.map((book, index) => (
              <Book name={book[0]} by={book[1]} img={book[2]} key={index} />
            ))
          }

        </div>
      </div>
    </div>
  )
}

export default Search