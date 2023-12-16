// App.js
import React from 'react';
import GoBoard from './components/GoBoard';

const App = () => {
  const handleClick = (rowIndex, colIndex) => {
    // Do something with the clicked coordinates
    console.log(`Clicked on cell at (${rowIndex}, ${colIndex})`);
  };

  const boardState = [
    [7, 3, 3, 3, 3, 3, 3, 3, 8],
    [5, 0, 0, 0, 0, 0, 0, 0, 6],
    [5, 0, 0, 0, 0, 0, 0, 0, 6],
    [5, 0, 0, 0, 0, 0, 0, 0, 6],
    [5, 0, 0, 0, 11, 0, 0, 0, 6],
    [5, 0, 0, 0, 0, 0, 0, 0, 6],
    [5, 0, 0, 0, 0, 0, 0, 0, 6],
    [5, 0, 0, 0, 0, 0, 0, 0, 6],
    [9, 4, 4, 4, 4, 4, 4, 4, 10],
  ];

  return (
    <div>
      <GoBoard boardState={boardState} onClick={handleClick} />
    </div>
  );
};


export default App;
