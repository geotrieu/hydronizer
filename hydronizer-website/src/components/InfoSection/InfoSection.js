import React, {Component} from 'react';
import { getWaterLeft, getMetrics } from '../../services/hydranatorService';
import './InfoSection.css'
import img1 from './image-1.JPG'
import img2 from './image-2.JPG'
import img3 from './image-3.JPG'
import img4 from './image-4.JPG'
class InfoSection extends Component {
    state = {
        waterLeft: "---",
        numSips: "---",
        waterDrankTotal: "---",
        waterDrankToday: "---"
    }

    async componentDidMount() {
        await this.getWaterLeft();
        await this.getMetrics();
    }

    async getWaterLeft() {
        let {data: waterLeft} = await getWaterLeft(this.props.device);
        this.setState({waterLeft: waterLeft.quantity});
    }

    async getMetrics() {
        let {data: metrics} = await getMetrics(this.props.device);
        this.setState({numSips: metrics.number_of_sips});
        this.setState({waterDrankTotal: metrics.total_consumed});
        this.setState({waterDrankToday: metrics.total_consumed_today});
    }

    render() {
        let { waterLeft, numSips, waterDrankToday, waterDrankTotal } = this.state;
        return (
            <div className="grid-container">
                <div className="Image-1"><img src={img1} alt="Bottle"/></div>
                <div className="Image-2"><img src={img2} alt="Bottle"/>
                    <h1>{waterDrankToday / 1000} L</h1>
                    <h2>of Water Drank Today</h2>
                </div>
                <div className="Info">
                    <medium> The human body is 60% water,
                        so it's important to stay
                        hydrated. Health experts
                        recommend a daily liquid
                        consumption of 2 litres per day</medium>
                </div>
                <div className="Dashboard">
                    <h2>Your Water Statistics</h2>
                    <h3>Number of Sips Today</h3>
                    <small>{numSips}</small>
                    <h3>Total Water Consumed</h3>
                    <small>{waterDrankTotal / 1000} L</small>
                    <h3>Water Left in Water Bottle</h3>
                    <small>{waterLeft} mL</small>
                </div>
                
                <div className="Image-4"><img src={img4} alt="Bottle"/></div>
            </div>
        )
    }
}

export default InfoSection