import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.sass'
import Header from './components/Header/Header'
import Footer from './components/Footer/Footer'
import Headbook from './components/Headbook/Headbook'
import { Routes, Route, Link } from 'react-router-dom'
import Layout from './components/Layout/Layout'
import Homepage from './components/Homepage/Homepage'
import Login from './components/Login/Login'

function App() {
  return (
    <>
        <Routes>
          <Route path='/' element={<Layout/>}>
            <Route index element={<Homepage />} />
            <Route path='/Headbook/*' element={<Headbook/>} />
            <Route path='/Login' element={<Login />}></Route>
          </Route>
        </Routes>
      <Footer />
    </>
  )
}

export default App
