import { combineReducers } from '@reduxjs/toolkit';
import friendsSlice from './reducers/friendsSlice';
import authReducer from './reducers/isAuthSlice';
import userReducer from './reducers/userSlice';
import socketsReducer from './reducers/isSocketsActive';
import menusReduce from './reducers/isMenusActiveSlice';
import gameReducer from './reducers/gameSlice';
import gameAcceptReducer from './reducers/gameAcceptingSlice'
import settingsReducer from './reducers/settingsSlice'

const rootReducer = combineReducers({
  friendsSlice,
  authReducer,
  userReducer,
  socketsReducer,
  menusReduce,
  gameReducer,
  gameAcceptReducer,
  settingsReducer
});

export default rootReducer;
