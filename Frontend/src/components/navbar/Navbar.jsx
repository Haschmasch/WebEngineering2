/* Navbar with all Categories and Subcategories.
The Subcategories show up after hovering over the associated Category */

import React, {useEffect, useState} from "react";
import {AiOutlineHeart, AiOutlineUser} from "react-icons/ai";
import {CiLogin, CiLogout} from "react-icons/ci";
import {Link} from "react-router-dom";
import "./Navbar.css";

import Searchbar from "../searchbar/Searchbar";
import {Logout} from "../pages/auth/Logout";
import {getCategories, getCategory} from "../../fetchoperations/CategoriesOperations";
import {isLoggedIn} from "../utils/StorageInterface";
import UserChat from "../pages/user/UserChat";

export default function  Navbar() {
    const [categories, setCategories] = useState([]);

    useEffect(() => {
        getCategories().then(r => setCategories(r))
    }, []);

    return (
        <>
            <div className="main-header">
                <div className="container">
                    <a href="/" className="logo">GenuineGoods
                    </a>
                    <div className="search-bar-container">
                        <div>
                            <Searchbar/>
                        </div>
                    </div>
                    <div className="icon">
                        {isLoggedIn() && (
                            <>
                                <div className="fa-icon">
                                    <Link to="/profile" className="link">
                                        <AiOutlineUser/>
                                    </Link>
                                </div>
                                <div className="fa-icon">
                                    <Link to="/followings" className="link">
                                        <AiOutlineHeart/>
                                    </Link>
                                </div>
                            </>
                        )}
                        {isLoggedIn() ? (
                            <>
                                <UserChat/>
                                <div className="fa-icon">
                                    <Link className="link">
                                        <CiLogout onClick={() => Logout()}/>
                                    </Link>
                                </div>
                            </>
                        ) : (
                            <div className="fa-icon">
                                <Link to="/signin" className="link">
                                    <CiLogin/>
                                </Link>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            <div className="header">
                <div className="container">
                    <nav>
                        <ul className="categories">
                            {categories.map(category => (
                                <NavbarItem category={category} key={category.id}/>
                            ))}
                        </ul>
                    </nav>
                </div>
            </div>
        </>
    );
};

const NavbarItem = ({
                        category
                    }) => {
    const [isDropdownVisible, setDropdownVisible] = useState(false);

    const handleMouseEnter = () => {
        setDropdownVisible(true);
    };

    const handleMouseLeave = () => {
        setDropdownVisible(false);
    };

    return (
        <li key={"cat" + category.id}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
        >
            <Link to={`category/${category.id}`} className="nav-item" id="dropbtn">
                {category.name}
            </Link>
            {isDropdownVisible && <SubCatDropdown category_id={category.id}/>}
        </li>
    );
};

const SubCatDropdown = ({
                            category_id
                        }) => {
    const [subcategories, setSubcategories] = useState([]);

    useEffect(() => {
        const response = getCategory(category_id);
        if (response) {
            response
                .then((data) => {
                    setSubcategories(data.related_subcategories || []);
                })
                .catch((error) => console.error(error));
        }
    }, [category_id]);

    if (subcategories.length === 0) {
        return null;
    }

    return (
        <ul className="dropdown-content">
            {subcategories.map((subcategory) => (
                <li key={"sub" + subcategory.id}>
                    <Link
                        to={`category/${category_id}/subcategory/${subcategory.id}`}
                        className="link"
                    >
                        {subcategory.name} <br/>
                    </Link>
                </li>
            ))}
        </ul>
    );
};
