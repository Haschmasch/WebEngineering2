/* Creates Footer with associated Footersites and socialmedia links */

import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faFacebook, faInstagram} from "@fortawesome/free-brands-svg-icons";
import "./Footer.css";

import {Link} from "react-router-dom";
import Copyright from "../utils/Copyright";

export default function Footer() {
    return (
        <div className='footer-container'>
            <div className='footer-links'>
                <div className='footer-link-wrapper'>
                    <div className='footer-link-items'>
                        <h2>Über uns</h2>
                        <Link to='/unserteam'>Unser Team</Link>
                        <Link to='/vision'>Vision</Link>
                    </div>
                    <div className='footer-link-items'>
                        <h2>Informationen</h2>
                        <Link to='/datenschutz'>Datenschutzerklärung</Link>
                        <Link to='/impressum'>Impressum</Link>
                    </div>
                    <div className='footer-link-items'>
                        <h2>Social Media</h2>
                        <Link to='https://www.instagram.com/'
                              target='_blank'>Instagram</Link>
                        <Link to='https://www.facebook.com/'
                              target='_blank'>Facebook</Link>
                    </div>
                </div>
            </div>
            <section className='social-media'>
                <div className='social-media-wrap'>
                    <div className='footer-logo'>
                        <Link to='/' className='social-logo'>
                            <img src="./logo.png" alt="Logo" className='logo'/>
                        </Link>
                    </div>
                    <small className='website-rights'><Copyright/></small>
                    <div className='social-icons'>
                        <Link
                            className='social-icon-link facebook'
                            to='https://www.facebook.com/'
                            target='_blank'
                            aria-label='Facebook'
                        >
                            <FontAwesomeIcon icon={faFacebook}/>
                        </Link>
                        <Link
                            className='social-icon-link instagram'
                            to='https://www.instagram.com/'
                            target='_blank'
                            aria-label='Instagram'
                        >
                            <FontAwesomeIcon icon={faInstagram}/>
                        </Link>
                    </div>
                </div>
            </section>
        </div>
    );
};