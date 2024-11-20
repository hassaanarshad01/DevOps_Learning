import React from "react";
import { Button } from "antd";
import { Link } from "react-router-dom";

const HeaderComponent = () => {
    return (
        <>
        <header className="App-header">
            <h1>ReartifyAI</h1>

            <nav className="App-nav-container">
            <div className="App-nav">
            <Button type="primary">
                <Link to="/">Home</Link>
            </Button>
            <Button type="primary">
                <Link to="/generate">Inpaint</Link>
            </Button>
            <Button type="primary">Models' Information</Button>

            </div>
            <div className="App-nav-2">
            <Button type="primary">Sign in</Button>
            <Button type="primary">Register</Button>
            </div>
        </nav>
        </header>
        </>
    )
}
export default HeaderComponent