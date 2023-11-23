import React from 'react';
import { Avatar, Typography } from '@mui/material';
import './SellerInfo.css';

function SellerInfo({ seller }) {
    if (!seller) {
        return null;
    }

    return (
        <div className="seller-info">
            <Typography variant="h6">Verkäuferinformationen</Typography>
            <div className="seller-details">
                <Avatar src={seller.avatar} alt={seller.name} />
                <div className="seller-description">
                    <Typography variant="body1">{seller.name}</Typography>
                    <Typography variant="body2">{seller.location}</Typography>
                </div>
            </div>
        </div>
    );
}

export default SellerInfo;
