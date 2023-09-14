import { combineReducers } from "@reduxjs/toolkit";
import authReducer from './reducers/isAuthSlice'
import userReducer from './reducers/userSlice'

const rootReducer = combineReducers({
  authReducer,
  userReducer
})

export default rootReducer