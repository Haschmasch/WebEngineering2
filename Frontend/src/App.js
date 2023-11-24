import React from "react";
import {Route, Routes} from "react-router-dom";
import {PrivateRoute} from "./components/pages/PrivateRoute"
import "./App.css";

import Navbar from "./components/navbar/Navbar";
import Footer from "./components/footer/Footer";
import Datenschutz from "./components/footer/footersites/Datenschutzerklaerung";
import Impressum from "./components/footer/footersites/Impressum";
import Unserteam from "./components/footer/footersites/UnserTeam";
import Vision from "./components/footer/footersites/Vision";

import SignInPage from "./components/pages/auth/SignIn";
import SignUpPage from "./components/pages/auth/SignUp";

import Chat from "./components/pages/chat/Chat";
import UserProfile from "./components/pages/user/UserProfile";

import Categories from "./components/pages/categorypages/Categories";
import Subcategories from "./components/pages/categorypages/Subcategories";

import Following from "./components/pages/following/Following";
import SearchPageListing from "./components/pages/search/SearchPageListing";
import AddOffer from "./components/pages/offer/AddOffer";
import OfferView from "./components/pages/offer/OfferView";

import Home from "./components/pages/home/Home";
import UserOffers from "./components/pages/user/UserOffers";

export default function App() {
    return (
        <>
            <Navbar/>
            <div className="fill-content">
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/offer/:offer_id" element={<OfferView/>}/>
                    <Route path="/category/:category_id" element={<Categories/>}/>
                    <Route path="/category/:category_id/subcategory/:subcategory_id" element={<Subcategories/>}/>
                    <Route path="/search/:search_String" element={<SearchPageListing/>}/>
                    <Route element={<PrivateRoute/>}>
                        <Route path="chats/:offer_id/:chat_id" element={<Chat/>}/>
                        <Route path="/profile" element={<UserProfile/>}/>
                        <Route path="/addOffer" element={<AddOffer/>}/>
                        <Route path="/followings" element={<Following/>}/>
                    </Route>
                    <Route path="/signin" element={<SignInPage/>}/>
                    <Route path="/signup" element={<SignUpPage/>}/>
                    <Route path="/datenschutz" element={<Datenschutz/>}/>
                    <Route path="/impressum" element={<Impressum/>}/>
                    <Route path="/unserteam" element={<Unserteam/>}/>
                    <Route path="/vision" element={<Vision/>}/>
                    <Route path="/userOffers" element={<UserOffers/>}/>
                </Routes>
            </div>
            <Footer/>
        </>
    );
};