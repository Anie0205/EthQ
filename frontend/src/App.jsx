import React from 'react'
import FileUpload from './components/FileUpload.jsx'
import './App.css'

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <h1>ETHQ</h1>
        <p>ETHICAL QUIZ GENERATOR</p>
      </header>
      <main className="app-main">
        <FileUpload />
      </main>
    </div>
  )
}

export default App
