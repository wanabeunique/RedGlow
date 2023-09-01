import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.sass'
import 'normalize.css'
import { BrowserRouter } from 'react-router-dom'
import store from './store/store.js'
import { Provider } from 'react-redux'

ReactDOM.createRoot(document.getElementById('root')).render(
  // <React.StrictMode>
  <Provider store={store}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </Provider>
  // </React.StrictMode>,
)
