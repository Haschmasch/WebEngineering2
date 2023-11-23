import React, {useState} from 'react';
import {IconButton} from "@mui/material";
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';

function Slideshow(props) {
    const [currentIndex, setCurrentIndex] = useState(0);
    if (props) {
        const {offer, imageNames} = props

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
                <div className="slideshow__container">
                    <img src={getImageLink()} alt={`Slide ${currentIndex}`} />
                </div>
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
    }

    return (
        <div className="slideshow">

        </div>
    );
}

export default Slideshow;
