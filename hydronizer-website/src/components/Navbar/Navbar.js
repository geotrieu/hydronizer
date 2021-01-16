import React, { Component } from 'react';
import { MenuItems } from "./MenuItems";
import './Navbar.css'
import 
class Navbar extends Component {
    render() {
        return(
            <nav className="NavbarItems">
                <h1 className="navbar-logo">Hydronizer<i className="fab fa-react"></i></h1>
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