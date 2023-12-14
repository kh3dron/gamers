// App.js
import React from 'react';
import GoBoard from './components/GoBoard';

const App = () => {
  const boardState = [[7, 3, 3, 3, 3, 3, 3, 3, 8], [5, 0, 2, 0, 0, 0, 0, 0, 6], [5, 2, 1, 2, 0, 0, 0, 0, 6], [5, 0, 2, 0, 2, 2, 0, 0, 6], [5, 0, 0, 2, 11, 1, 2, 0, 6], [5, 0, 0, 0, 2, 1, 2, 0, 6], [5, 0, 0, 0, 0, 2, 0, 0, 6], [5, 0, 0, 0, 0, 0, 0, 0, 6], [9, 4, 4, 4, 4, 4, 4, 4, 10]];

  return (
    <div>
      <h1>Go Board</h1>
      <GoBoard boardState={boardState} />
    </div>
  );
};

export default App;
