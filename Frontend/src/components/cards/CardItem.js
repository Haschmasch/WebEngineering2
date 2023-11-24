/* Contains individual Offers from the Overview and summarizes them in a Box,
* usage of MUI library */

import React, {useState} from 'react';
import {Link} from 'react-router-dom';
import Button from "@mui/material/Button";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import {addFollowing, deleteFollowing} from "../../fetchoperations/FollowingsOperations";
import {isLoggedIn} from "../utils/StorageInterface";

const styleButton = {
    "&:active": {},
    "&:hover": {
        backgroundColor: "white",
        color: "red"
    },
    color: "#466481",
};

export default function CardItem(props) {
    const [hover, setHover] = useState(false);
    const handleClick = (e) => {
        e.preventDefault()

        if (props.followings.some(following => following.offer_id === props.offer_id)) {
            deleteFollowing(props.followings.filter(following => following.offer_id === props.offer_id)[0].id).then(() => props.setNewFetch(fetch => fetch + 1))
            return;
        }

        addFollowing(props.offer_id).then(() => props.setNewFetch(fetch => fetch + 1))

    }

    function getImageLink() {
        return `http://localhost:8000/offers/${props.offer_id}/thumbnail`
    }

    return (
        <>
            <li className='cards__item'>
                <Link className='cards__item__link' to={props.path} id={props.id}>
                    <figure className='cards__item__pic-wrap' data-category={props.label}>
                        <img
                            className='cards__item__img'
                            alt={props.alt}
                            src={getImageLink()}
                        />
                    </figure>
                    <div className='cards__item__info'>
                        <h5 className='cards__item__text'>{props.text}</h5>
                        {isLoggedIn() && (
                            <Button disableRipple sx={styleButton} variant="text" onClick={(e) => handleClick(e)}
                                    onMouseLeave={() => setHover(false)} onMouseEnter={() => setHover(true)}
                            >
                                {
                                    props.followings.some(following => following.offer_id === props.offer_id) ? (
                                        hover ? (<FavoriteBorderIcon/>) :
                                            (<FavoriteIcon sx={{color: 'red'}}/>)
                                    ) : (hover ? (<FavoriteIcon sx={{color: "red"}}/>) :
                                        (<FavoriteBorderIcon/>))
                                }


                            </Button>)
                        }
                    </div>
                </Link>
            </li>
        </>
    );
}

