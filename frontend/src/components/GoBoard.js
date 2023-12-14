// GoBoard.js
import React from 'react';

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

const GoBoard = ({ boardState }) => {
  const cellSize = 70; // Adjust the size as needed

  const assetStyles = {
    cell: {
      width: `${cellSize}px`,
      height: `${cellSize}px`,
      position: 'relative',
      overflow: 'hidden', // Ensure child elements don't overflow the cell
    }
  };

  const handleCellClick = (rowIndex, colIndex) => {
    // Pass the clicked coordinates to the parent component
    onCellClick(rowIndex, colIndex);
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: `repeat(${boardState.length}, ${cellSize}px)` }}>
      {boardState.map((row, rowIndex) =>
        row.map((cell, colIndex) => (
          <div key={`${rowIndex}-${colIndex}`} style={assetStyles.cell}>
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
