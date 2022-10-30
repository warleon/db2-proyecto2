import { useState, useEffect } from 'react'

const Searcher = (props) => {
    
    const [query, setQuery] = useState({text: "", topk: ""})

    useEffect(() => {
        console.log(query)
    }, [query])

    const handleChange = (event) => {
        const {name, value} = event.target
        setQuery((prev) => {
            return {
                ...prev,
                [name]: value
            }
        })
    }

    const handleSubmit = (event) => {
        event.preventDefault()
        props.submitQuery(query)
    }
    
    return (
        <form onSubmit={handleSubmit} className='searcher-form'>
            <textarea className="searcher-text-input" onChange={handleChange} name="text" value={query.text} placeholder="Write your query here"></textarea>
            <div className='submit-div'>
                <input className="searcher-topk-input" onChange={handleChange} name="topk" type="number" min="0" value={query.topk} placeholder="Top K"></input>
                <button>Submit</button>
            </div>
        </form>
    )
}

export default Searcher