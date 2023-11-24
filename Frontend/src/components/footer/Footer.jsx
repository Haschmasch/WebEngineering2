import React from "react";
import "./FooterStyles.css"

import {Link} from "react-router-dom";

const Footer = () => {
    return (
        <>
            <div className="footer-box">
                <div className="footer-container">
                    <div className="row">
                        <div className="column">
                            <div className="heading">
                                GENUINE GOODS
                            </div>
                            <img className="image" src="/logo.png" alt="logo"></img>
                        </div>
                        <div className="column" style={{paddingLeft: "45px"}}>
                            <div className="heading">
                                ÜBER UNS
                            </div>
                            <Link to="/unserteam" className="Links">
                                Unser Team
                            </Link>
                            <Link to="/vision" className="Links">
                                Vision
                            </Link>
                        </div>
                        <div className="column">
                            <div className="heading">
                                INFORMATIONEN
                            </div>
                            <Link to="/datenschutz" className="Links">
                                Datenschutzerklärung
                            </Link>
                            <Link to="/impressum" className="Links">
                                Impressum
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};
export default Footer;