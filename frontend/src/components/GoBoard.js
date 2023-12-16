// GoBoard.js
import React, { useEffect, useState } from 'react';

import black from './assets/b.png';
import white from './assets/w.png';
import empty from './assets/e.png';

import down from './assets/d.png';
import up from './assets/u.png';
import left from './assets/l.png';
import right from './assets/r.png';

import ul from './assets/ul.png';
import ur from './assets/ur.png';
import dl from './assets/dl.png';
import dr from './assets/dr.png';

import s from './assets/s.png';

const GoBoard = ({ onClick }) => {
  const cellSize = 70; // Adjust the size as needed

  const assetStyles = {
    cell: {
      width: `${cellSize}px`,
      height: `${cellSize}px`,
      position: 'relative',
      overflow: 'hidden', // Ensure child elements don't overflow the cell
      cursor: 'pointer', // Set cursor to pointer to indicate clickable
    }
  };

  const [boardState, setBoardState] = useState([]);

  useEffect(() => {
    // Fetch initial board state from localhost:3001/get_board
    fetch('http://localhost:3001/get_board')
      .then(response => response.json())
      .then(data => setBoardState(data))
      .catch(error => console.error('Error fetching initial board state:', error));
  }, []); // Empty dependency array to run the effect only once

  const handleCellClick = (rowIndex, colIndex) => {
    fetch('http://localhost:3001/place_stone', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        move: { row: rowIndex, col: colIndex },
      }),
    })
      .then(response => response.json())
      .then(updatedState => {
        // Update the board state with the response
        setBoardState(updatedState);
        // Call the provided onClick callback
        onClick(rowIndex, colIndex);
      })
      .catch(error => console.error('Error updating board state:', error));
  };  

  return (
    <div style={{ display: 'grid', gridTemplateColumns: `repeat(${boardState.length}, ${cellSize}px)` }}>
      {boardState.map((row, rowIndex) =>
        row.map((cell, colIndex) => (
          <div key={`${rowIndex}-${colIndex}`} style={assetStyles.cell} onClick={() => handleCellClick(rowIndex, colIndex)}>
            {cell === 0 && <img src={empty} alt="Empty" style={assetStyles.cell} />}
            {cell === 1 && <img src={white} alt="White" style={assetStyles.cell} />}
            {cell === 2 && <img src={black} alt="Black" style={assetStyles.cell} />}

            {cell === 3 && <img src={up} alt="Up" style={assetStyles.cell} />}
            {cell === 4 && <img src={down} alt="Down" style={assetStyles.cell} />}
            {cell === 5 && <img src={left} alt="Left" style={assetStyles.cell} />}
            {cell === 6 && <img src={right} alt="Right" style={assetStyles.cell} />}

            {cell === 7 && <img src={ul} alt="Up Left" style={assetStyles.cell} />}
            {cell === 8 && <img src={ur} alt="Up Right" style={assetStyles.cell} />}
            {cell === 9 && <img src={dl} alt="Down Left" style={assetStyles.cell} />}
            {cell === 10 && <img src={dr} alt="Down Right" style={assetStyles.cell} />}

            {cell === 11 && <img src={s} alt="Star" style={assetStyles.cell} />}
          </div>
        ))
      )}
    </div>
  );
};

export default GoBoard;
