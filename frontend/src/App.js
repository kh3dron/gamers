// App.js
import React from 'react';
import GoBoard from './components/GoBoard';

const App = () => {
  const handleClick = (rowIndex, colIndex) => {
    // Do something with the clicked coordinates
    console.log(`Clicked on cell at (${rowIndex}, ${colIndex})`);
  };

  const boardState = [];

  return (
    <div>
      <GoBoard boardState={boardState} onClick={handleClick} />
    </div>
  );
};


export default App;
