import React from 'react';
import './InfoSection.css'

const InfoSection = () => {
    return (
        <div class="grid-container">
            <div class="Image-1"></div>
            <div class="Image-2">
                <h1>1.1L</h1>
                <h2>of Water Drank Today</h2>
            </div>
            <div class="Info">
                <small> The human body is 60% water,
                    so it's important to stay
                    hydrated. Health experts
                    recommend a daily liquid
                    consumption of 2 litres per day</small>
            </div>
            <div class="Dashboard">
                <h2>Your Water Statistics</h2>
                <h3>Number of Sips Today</h3>
                <small>10</small>
                <h3>Average Daily Water Consumption</h3>
                <small>1.5L</small>
                <h3>Number of Days You've Reached the Recommended Daily Consumption</h3>
                <small>25 days</small>
            </div>
            <div class="Image-3"></div>
            <div class="Image-4"></div>
        </div>
    )
}

export default InfoSection