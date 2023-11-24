import React from "react";
import "./SearchResult.css";
import {Link} from "react-router-dom";

export const SearchResult = ({result}) => {
    return (
        <Link to={`/offer/${result.id}`} >
            <div className="search-result">
                {result.title}
            </div>
        </Link>
    );
};
