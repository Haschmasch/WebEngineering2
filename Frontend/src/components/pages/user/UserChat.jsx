/* creates Chat, is associated to an Offer and an User */

import React, {useEffect, useState} from "react";
import Box from '@mui/material/Box';
import '../../navbar/Navbar.css';
import SwipeableDrawer from '@mui/material/SwipeableDrawer';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import MailIcon from '@mui/icons-material/Mail';
import SmsIcon from "@mui/icons-material/Sms";
import {Link} from "react-router-dom";
import {getAllChatsInvolvingUser} from "../../../fetchoperations/ChatsOperations";
import {getOffer} from "../../../fetchoperations/OffersOperations";
import {getUser} from "../../../fetchoperations/UsersOperation";
import {getUser_id} from "../../utils/StorageInterface";
import {MailOutline} from "@mui/icons-material";

export default function UserChat() {
    const [state, setState] = useState({
        right: false,
    });
    const [chats, setChats] = useState([]);
    useEffect(() => {

        try {
            getAllChatsInvolvingUser().then(result => {
                if (result.length === 0) {
                    setChats([]);
                } else {
                    Promise.all(result.flat().map(async (chat) => {
                        try {
                            const offer = await getOffer(chat.offer_id);
                            const user = await getUser(chat.creator_id);
                            const ownOffer = user.id === getUser_id();
                            return {chat, offer, user, ownOffer};
                        } catch (error) {
                            return null;
                        }
                    })).then(chatDetails => setChats(chatDetails.filter((detail) => detail !== null)));
                }
            });
        } catch (error) {
            return null;
        }
    }, []);

    const toggleDrawer = (anchor, open) => (event) => {
        if (
            event &&
            event.type === 'keydown' &&
            (event.key === 'Tab' || event.key === 'Shift')
        ) {
            return;
        }

        setState({...state, [anchor]: open});
    };

    const list = (anchor) => (
            <Box
                sx={{width: 250}}
                role="presentation"
                onClick={toggleDrawer(anchor, false)}
                onKeyDown={toggleDrawer(anchor, false)}
            >
                <List>
                    {chats.map((chatDetail, index) => (
                        chatDetail.ownOffer && (
                            <ListItem key={chatDetail.id} disablePadding>
                                <ListItemButton>
                                    <Link to={`/chats/${chatDetail.offer.id}/${chatDetail.chat.id}`}>
                                        <ListItemIcon>
                                            <MailOutline/>
                                        </ListItemIcon>
                                        Verkäufer: {chatDetail.offer.related_user?.name} |
                                        Angebot: {chatDetail.offer?.title}
                                    </Link>
                                </ListItemButton>
                            </ListItem>
                        )))}
                </List>
                <Divider/>
                <List>
                    {chats.map((chatDetail, index) => (
                        !chatDetail.ownOffer && (
                            <ListItem key={chatDetail.id} disablePadding>
                                <ListItemButton>
                                    <Link to={`/chats/${chatDetail.offer.id}/${chatDetail.chat.id}`}>
                                        <ListItemIcon>
                                            <MailIcon/>
                                        </ListItemIcon>
                                        Dein Angebot: {chatDetail.offer?.title}
                                    </Link>
                                </ListItemButton>
                            </ListItem>
                        )))}
                </List>
            </Box>
        )
    ;

    return (
        <div>
            <Link onClick={toggleDrawer('right', true)}>{<>
                <div className="fa-icon">
                    <div className="link">
                        <SmsIcon/>
                    </div>
                </div>
            </>}</Link>
            <SwipeableDrawer
                anchor='right'
                open={state['right']}
                onClose={toggleDrawer('right', false)}
                onOpen={toggleDrawer('right', true)}
            >
                {list('right')}
            </SwipeableDrawer>
        </div>
    );
}