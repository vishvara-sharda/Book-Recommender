import React from 'react'
import "./loader.css"
import { Widgets } from '@mui/icons-material'

function Loader() {
    return (
        <div style={{width: "100%"}}>
            <div class="hourglassBackground">
                <div class="hourglassContainer">
                    <div class="hourglassCurves"></div>
                    <div class="hourglassCapTop"></div>
                    <div class="hourglassGlassTop"></div>
                    <div class="hourglassSand"></div>
                    <div class="hourglassSandStream"></div>
                    <div class="hourglassCapBottom"></div>
                    <div class="hourglassGlass"></div>
                </div>
            </div>
        </div>
    )
}

export default Loader
