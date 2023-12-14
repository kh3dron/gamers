// App.js
import React from 'react';
import GoBoard from './components/GoBoard';

const App = () => {
  const boardState = [
    [1, 2, 3],
    [3, 1, 2],
    [2, 3, 1],
  ];

  return (
    <div>
      <h1>Go Board</h1>
      <GoBoard boardState={boardState} />
    </div>
  );
};

export default App;
