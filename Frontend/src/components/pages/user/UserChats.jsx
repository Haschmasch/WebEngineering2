import React, {useEffect, useState} from 'react';
import {getAllChatsInvolvingUser} from "../../../fetchoperations/ChatsOperations";
import './UserChats.css';
import {Link} from 'react-router-dom';
import {getOffer} from "../../../fetchoperations/OffersOperations";
import {getUser_id} from "../../utils/StorageInterface";
import {getUser} from "../../../fetchoperations/UsersOperation";
import Button from "@mui/material/Button";

const UserChats = () => {
    const [chats, setChats] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const result = await getAllChatsInvolvingUser();
                if (result.length === 0) {
                    setChats([]);
                } else {
                    const chatDetails = await Promise.all(
                        result.flat().map(async (chat) => {
                            try {
                                const offer = await getOffer(chat.offer_id);
                                const user =
                                    chat.creator_id === getUser_id()
                                        ? {name: 'Du'}
                                        : await getUser(chat.creator_id);
                                return {chat, offer, user};
                            } catch (error) {
                                return null;
                            }
                        })
                    );
                    const filteredChatDetails = chatDetails.filter((detail) => detail !== null);
                    setChats(filteredChatDetails);
                }
            } catch (error) {
                return null;
            }
        };

        if (chats.length === 0) {
            fetchData();
        }
    });

    // const createChat = async () => {
    //
    //     getChatsByUser().then(chats => chats.some(chat => chat.offer_id === parseInt(offer_id) && chat.creator_id === getUser_id())).then(bool => {
    //         if (!bool) {
    //             addChat(offer_id).then(r => {
    //                 console.log('Chat erfolgreich erstellt.');
    //                 navigate(`/chats/${offer_id}/${r.id}`)
    //
    //             }, (r) => {
    //                 console.log('Fehler beim Erstellen des Chats: ', r.detail);
    //             })
    //             return
    //         }
    //         getChatsByUser().then(chats => {
    //             console.log(chats);
    //             return chats.filter(chat => chat.offer_id === parseInt(offer_id) && chat.creator_id === getUser_id())[0]}).then(r => {
    //             console.log(r);
    //             navigate(`/chats/${offer_id}/${r.id}`)})
    //     })
    // };

    return (
        <div className="chats">
            {chats.length === 0 ? (
                <p>Du hast keine offenen Chats.</p>
            ) : (
                <ul>
                    {chats.map((chatDetail, index) => (
                        <li key={index}>
                            <Button
                                variant="outlined"
                                sx={{ width: 'auto', height: '40px', maxWidth:"50%"}}
                            >
                                <Link to={`/chats/${chatDetail.offer.id}/${chatDetail.chat.id}`} >
                                    Verkäufer: {chatDetail.offer.related_user?.name || 'Unbekannt'} |{' '}
                                    Angebot: {chatDetail.offer?.title || 'Unbekannt'}
                                </Link>
                            </Button>
                            {/*<Link to={`/chats/${chatDetail.offer.id}/${chatDetail.chat.id}`}>
                                <strong>Verkäufer:</strong> {chatDetail.offer.related_user?.name || 'Unbekannt'} |{' '}
                                <strong>Angebot:</strong> {chatDetail.offer?.title || 'Unbekannt'}
                            </Link>*/}
                        </li>

                    ))}
                </ul>
            )}
        </div>
    );
};
export default UserChats;