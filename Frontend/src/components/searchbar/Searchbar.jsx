import React, {useEffect, useState} from "react";
import "./Searchbar.css";
import {FaSearch} from "react-icons/fa";
import {getOffersBySubstring} from "../../fetchoperations/SearchOperations";
import SearchResults from "./SearchResultsList";
import {useNavigate} from "react-router-dom";

export const Searchbar = () => {
    const [input, setInput] = useState("");
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        if (input.length > 0) {
            setLoading(true);
            getOffersBySubstring(input).then(r => setResults(r)).finally(() => setLoading(false));
            return
        }
        setResults([])
    }, [input]);

    function onEnterPress(e) {
        if (e.code === "Enter") {
            setInput('')
            navigate(`/search/${input}`)
        }
    }

    return (
        <>
            <div className="input-wrapper">
                <FaSearch id="search-icon"/>
                <input
                    placeholder="Suche"
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyUp={e => onEnterPress(e)}
                />
            </div>
            <SearchResults results={results} loading={loading}/>
        </>
    );
};

export default Searchbar;
