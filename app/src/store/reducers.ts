import { combineReducers } from "@reduxjs/toolkit";
import authReducer from './reducers/isAuthSlice'
import userReducer from './reducers/userSlice'
import socketsReducer from './reducers/isSocketsActive'
import friendsMenuReduce from './reducers/isfriendsMenuActiveSlice'

const rootReducer = combineReducers({
  authReducer,
  userReducer,
  socketsReducer,
  friendsMenuReduce
})

export default rootReducer