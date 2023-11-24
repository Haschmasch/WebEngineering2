import React, {useState} from 'react';
import {Card, CardMedia, IconButton} from "@mui/material";
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';

export default function Slideshow(props) {
    const {offer, imageNames} = props
    const [currentIndex, setCurrentIndex] = useState(0);

    function getImageLink() {
        return `http://localhost:8000/offers/${offer.id}/images/${imageNames[currentIndex]}`
    }

    const nextSlide = () => {
        setCurrentIndex(imageNames.length === 0 ? 0 : (currentIndex + 1) % imageNames.length);
    };

    const previousSlide = () => {
        setCurrentIndex(imageNames.length === 0 ? 0 : (currentIndex - 1 + imageNames.length) % imageNames.length);
    };

    let content = []
    if (offer && imageNames) {
        content = (
            <>
                <div className="slideshow__container">
                    <Card sx={{maxWidth: 500, maxHeight: 700}}>
                        <CardMedia component="img" image={getImageLink()} alt={`Slide ${currentIndex}`}
                                   sx={{width: 500, height: 700}}>
                        </CardMedia>
                    </Card>
                </div>
            </>
        );
    }

    return (
        <div className="slideshow">
            {content}
            <div className="slideshow__controls">
                <IconButton aria-label="Previous" size="large" onClick={previousSlide}>
                    <ArrowBackIosIcon fontSize="inherit"/>
                </IconButton>
                <IconButton aria-label="Next" size="large" onClick={nextSlide}>
                    <ArrowForwardIosIcon fontSize="inherit"/>
                </IconButton>
            </div>
        </div>
    );
};
