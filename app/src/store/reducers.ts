import { combineReducers } from "@reduxjs/toolkit";
import authReducer from './reducers/isAuthSlice'
import userReducer from './reducers/userSlice'
import socketsReducer from './reducers/isSocketsActive'

const rootReducer = combineReducers({
  authReducer,
  userReducer,
  socketsReducer
})

export default rootReducer