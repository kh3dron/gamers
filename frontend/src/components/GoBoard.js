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
  const [isProcessingMove, setIsProcessingMove] = useState(false);

  const cellSize = 50;

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
    fetch('http://localhost:3001/get_board')
      .then(response => response.json())
      .then(data => setBoardState(data))
      .catch(error => console.error('Error fetching initial board state:', error));
    getData();
  }, []);

  const handleCellClick = async (rowIndex, colIndex) => {
  if (isProcessingMove || boardState[rowIndex][colIndex] == 1 || boardState[rowIndex][colIndex] == -1) {
    // If processing move or there's already a stone, return early
    return;
  }

  const maxAttempts = 3; // Set the maximum number of retry attempts
  let attempts = 0;

  while (attempts < maxAttempts) {
    try {
      setIsProcessingMove(true);

      const response = await fetch('http://localhost:3001/place_stone', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          move: { row: rowIndex, col: colIndex },
        }),
      });

      const updatedState = await response.json();
      setBoardState(updatedState);
      onClick(rowIndex, colIndex);
      getData();
      await playRandom();
      getData();

      // If the above code runs without errors, break out of the loop
      break;
    } catch (error) {
      console.error('Error updating board state:', error);
      attempts++;

      // You can add a delay between retry attempts if needed
      // await new Promise(resolve => setTimeout(resolve, 1000));
    } finally {
      setIsProcessingMove(false);
    }
  }
};


  const resetGame = async () => {
    try {
      const response = await fetch('http://localhost:3001/reset', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      const updatedState = await response.json();
      setBoardState(updatedState);
      getData();

    } catch (error) {
      console.error('Error updating board state:', error);
    }
  };

  async function handlePassClick() {
  fetch('http://localhost:3001/pass', {
    method: 'PUT',
  })
    .then(response => response.json())
    .then(data => {
      const formattedJson = JSON.stringify(data, null, 2);
    })
    .catch(error => console.error('Error fetching data:', error));

    getData();
    await playRandom();
    getData();
}

  function getData() {
    fetch('http://localhost:3001/gamestats')
      .then(response => response.json())
      .then(data => {
        const formattedJson = JSON.stringify(data, null, 2);
        document.getElementById('boardState').innerHTML = `<pre style="white-space: pre-wrap;">${formattedJson}</pre>`;
      })
      .catch(error => console.error('Error fetching data:', error));
  }

  const playRandom = async (rowIndex, colIndex) => {
    try {
      const response = await fetch('http://localhost:3001/agent_random', {
        method: 'GET',
      });

      const updatedState = await response.json();
      setBoardState(updatedState);
      onClick(rowIndex, colIndex);
      getData();

    } catch (error) {
      console.error('Error uplaying random move:', error);
    }
  };

  return (
    <div style={{ display: 'flex' }}>
      <div style={{ flexShrink: 0, marginRight: '20px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: `repeat(${boardState.length}, ${cellSize}px)` }}>
          {boardState.map((row, rowIndex) =>
            row.map((cell, colIndex) => (
              <div key={`${rowIndex}-${colIndex}`} style={assetStyles.cell} onClick={() => handleCellClick((rowIndex), (colIndex))}>
                {cell === 0 && <img src={empty} alt="Empty" style={assetStyles.cell} />}
                {cell === 2 && <img src={white} alt="White" style={assetStyles.cell} />}
                {cell === 1 && <img src={black} alt="Black" style={assetStyles.cell} />}

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
      </div>

      <div>
        <button onClick={() => handlePassClick()}>Pass</button>
        <br />
        <button onClick={() => resetGame()}>Reset Game</button>
        <p>Board State:</p>
        <div id="boardState"></div>
      </div>
    </div>
  );
};

export default GoBoard;