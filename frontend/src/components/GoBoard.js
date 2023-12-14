import React from 'react';

const GoBoard = ({ boardState }) => {
  // Define the styles for each asset type
  const assetStyles = {
    1: { backgroundColor: 'black', borderRadius: '50%', width: '30px', height: '30px' },
    2: { backgroundColor: 'white', borderRadius: '50%', width: '30px', height: '30px' },
    3: { backgroundColor: 'orange', width: '30px', height: '30px' },
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: `repeat(${boardState.length}, 30px)` }}>
      {boardState.map((row, rowIndex) =>
        row.map((cell, colIndex) => (
          <div key={`${rowIndex}-${colIndex}`} style={{ ...assetStyles[cell], border: '1px solid #333' }} />
        ))
      )}
    </div>
  );
};

export default GoBoard;
