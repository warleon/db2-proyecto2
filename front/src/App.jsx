import { useState, useEffect } from 'react'
import Searcher from "./components/Searcher"
import Resulter from "./components/Resulter"
import axios from "axios"
import data from "./data"

function App() {

  const [datapy, setDatapy] = useState({items:[], time:0})
  const [datapo, setDatapo] = useState([""])

  const submitQuery = (q) => {
    fetch('/api/query' , {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
        'Access-Control-Allow-Origin': '*' 
      },
      body: JSON.stringify(q)
    })
    .then(response => response.json())
    .then(data => setDatapy(data));
  }

  return (
    <div className="App">
      <Searcher submitQuery={submitQuery}/>
      <div className='resulters-cont'>
        <Resulter title="Top K - Python" data={datapy}/>
        <div className='separator'></div>
        <Resulter title="Top K - PostgreSQL" data={data}/>
      </div>
    </div>
  )
}

export default App
