import React, { Component } from 'react';
import { MenuItems } from "./MenuItems";
import './Navbar.css'
import logo from './logo512.jpg'
class Navbar extends Component {
    render() {
        return(
            <nav className="NavbarItems">
                <h1 className="navbar-logo"><img src={logo} alt="logo" className="logo"/></h1>
                <div className="menu-icon">
                </div>
                <ul className="nav-menu">
                    {MenuItems.map((item, index) =>{
                        return(
                        <li key={index}>
                            <a className={MenuItems.cName} href={item.url}>
                            {item.title}
                            </a>
                        </li>
                        )
                    })}
                    
                </ul>
            </nav>
        )
    }
}

export default Navbar