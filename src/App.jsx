import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.sass'
import Header from './components/Header/Header'
import Footer from './components/Footer/Footer'
import Headbook from './components/Headbook/Headbook'
import { Routes, Route, Link } from 'react-router-dom'

function App() {
  return (
    <>
      <Header />
        <Routes>
          <Route path='/Headbook/*' element={<Headbook/>} />
        </Routes>
      <Footer />
    </>
  )
}

export default App
