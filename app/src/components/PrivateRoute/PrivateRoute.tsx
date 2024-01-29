import { Navigate } from 'react-router-dom';

const PrivateRoute = ({isAuth, children }) => {
  console.log('роут', isAuth, children)

  if (!isAuth) { return <Navigate to="/login" /> }
  else { return children }
};

export default PrivateRoute;

