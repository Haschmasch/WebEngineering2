import React from "react";
import {SearchResult} from "./SearchResult";
import {Paper, Skeleton} from "@mui/material";

export const MAX_SEARCH_RESULTS_LOADING = 4;

export default function SearchResultsList(props) {
    const {results, loading} = props;
    let content = [];
    if (loading) {
        content = Array(MAX_SEARCH_RESULTS_LOADING)
            .fill(1)
            .map((card, index) => (
                <Skeleton key={index} height={40}/>
            ))
    } else if (results) {
        content = results.map((result, id) => <SearchResult result={result} key={id}/>)
    }
    return (
        <Paper sx={{
            position: 'absolute', maxHeight: '500px',
            boxShadow: '0px 8px 16px 0px rgba(0,0,0,0.2)',
            zIndex: 9000,
            overflowY: 'scroll',
            width: '300px',
        }}>
            {content}
        </Paper>
    );
};
