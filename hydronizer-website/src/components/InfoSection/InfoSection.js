import React, {Component} from 'react';
import getLastWaterBreak from '../../services/hydranatorService';
import './InfoSection.css'
import img1 from './image-1.JPG'
import img2 from './image-2.JPG'
import img3 from './image-3.JPG'
import img4 from './image-4.JPG'
class InfoSection extends Component {
    state = {
        waterQuantity: "---"
    }

    async componentDidMount() {
        await this.getWaterQuantity();
    }

    async getWaterQuantity() {
        let {data: lastWaterBreak} = await getLastWaterBreak();
        this.setState({waterQuantity: lastWaterBreak.quantity});
    }

    render() {
        let { waterQuantity } = this.state;
        return (
            <div className="grid-container">
                <div className="Image-1"><img src={img1} alt="Bottle"/></div>
                <div className="Image-2"><img src={img2} alt="Bottle"/>
                    <h1>1.1L</h1>
                    <h2>of Water Drank Today</h2>
                </div>
                <div className="Info">
                    <small> The human body is 60% water,
                        so it's important to stay
                        hydrated. Health experts
                        recommend a daily liquid
                        consumption of 2 litres per day</small>
                </div>
                <div className="Dashboard">
                    <h2>Your Water Statistics</h2>
                    <h3>Number of Sips Today</h3>
                    <small>10</small>
                    <h3>Average Daily Water Consumption</h3>
                    <small>1.5L</small>
                    <h3>Water Left in Water Bottle</h3>
                    <small>{waterQuantity} mL</small>
                </div>
                <div className="Image-3"><img src={img3} alt="Bottle"/></div>
                <div className="Image-4"><img src={img4} alt="Bottle"/></div>
            </div>
        )
    }
}

export default InfoSection