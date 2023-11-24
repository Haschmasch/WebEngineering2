import React, {useEffect, useState} from 'react';
import {getAllChatsInvolvingUser} from "../../../fetchoperations/ChatsOperations";
import './UserChats.css';
import {Link} from 'react-router-dom';
import {getOffer} from "../../../fetchoperations/OffersOperations";
import {getUser_id} from "../../utils/StorageInterface";
import {getUser} from "../../../fetchoperations/UsersOperation";
import Button from "@mui/material/Button";

export default function UserChats() {
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

    return (<div className="chats">
            {chats.length === 0 ? (<p>Du hast keine offenen Chats.</p>) : (<ul>
                    {chats.map((chatDetail) => (<li key={chatDetail.chat.id}>
                            <Button
                                variant="outlined"
                                sx={[{width: 'auto', height: '40px', maxWidth: "50%"}, chatDetail.ownOffer ? {color: 'purple'} : {color: 'green'}]}
                            >
                                <Link to={`/chats/${chatDetail.offer.id}/${chatDetail.chat.id}`}>
                                    Verkäufer: {chatDetail.offer.related_user?.name} |
                                    Angebot: {chatDetail.offer?.title}
                                </Link>
                            </Button>
                        </li>

                    ))}
                </ul>)}
        </div>);
};