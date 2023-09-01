import { combineReducers } from "@reduxjs/toolkit";
import authReducer from './reducers/isAuthSlice'

const rootReducer = combineReducers({
  authReducer,
})

export default rootReducer