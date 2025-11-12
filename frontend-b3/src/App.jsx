// src/App.jsx
import './App.css'
import TabelaAcoes from './components/TabelaAcoes'

function App() {
  return (
    <div className="app-container">
      <header>
        <h1>📊 Projeto Cloud B3</h1>
        <p>Visualização de dados processados via Azure Functions</p>
      </header>
      
      <main>
        <TabelaAcoes />
      </main>
    </div>
  )
}

export default App