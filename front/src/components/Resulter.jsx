import { useState, useEffect } from 'react'

const Resulter = (props) => {

    const anselems = props.data.items.map((item, i) => {
        if(i < props.data.items.length - 1) {
            return (
                <div className='lidiv-cont' key={i+1}>
                    <div className='paper-num'>Paper {i+1}</div>
                    <div className='paper-title'>{item.title}</div>
                    <div className='paper-abstract'>{item.abstract}</div>
                    <div className='paper-score'>{item.score}</div>
                </div>) 
        }
        else {
            return (
                <div className='lidiv-cont-last' key={i+1}>
                    <div className='paper-num'>Paper {i+1}</div>
                    <div className='paper-title'>{item.title}</div>
                    <div className='paper-abstract'>{item.abstract}</div>
                    <div className='paper-score'>{item.score}</div>
                </div>) 
        }
    })

    return (
        <div className='papa'>
            <h2>{props.title}</h2>
            <div className='results-cont'>
                <div className='titles-cont'>
                    <div className='empty'></div>
                    <div className='title-title'>Title (link)</div>
                    <div className='title-abstract'>Abstract</div>
                    <div className='title-score'>Score</div>
                </div>
                <div className='elems-cont'>
                    {anselems}
                </div>
            </div>
            <p>Time: {props.data.time} s</p>
        </div>
    )
}

export default Resulter