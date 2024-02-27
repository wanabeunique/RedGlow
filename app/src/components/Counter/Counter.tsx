import { useState, useEffect } from 'react';

function Counter({ initialValue = 0, intervalTime = 1000, direction = true }) {
  const [count, setCount] = useState(initialValue);
  const [isRunning, setIsRunning] = useState(true);

  const increment = () => {
    setCount((prevCount) => prevCount + 1);
  };

  const decrement = () => {
    if (count > 0){
      setCount((prevCount) => prevCount > 0 ? prevCount - 1 : 0);
    }
  };

  useEffect(() => {
    let interval;
    if (isRunning) {
      if (direction){
        interval = setInterval(increment, intervalTime);
      }
      else{
        interval = setInterval(decrement, intervalTime);
      }
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval); 
  }, [isRunning, intervalTime]);

  const formatTime = (timeInSeconds) => {
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = timeInSeconds % 60;
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  };

  return <div>{formatTime(count)}</div>;
}

export default Counter;
