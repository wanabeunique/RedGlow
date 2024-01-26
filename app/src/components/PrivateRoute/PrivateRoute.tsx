import { Children } from 'react';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({isAuth, children }) => {
  console.log('роут', isAuth, Children)

  if (!isAuth) { return <Navigate to="/login" /> }
  else { return children }
};

export default PrivateRoute;

