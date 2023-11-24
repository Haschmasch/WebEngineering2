import React, {useEffect, useRef, useState} from 'react';
import './Chat.css';
import {deleteChat, getChat, getChats, getOwnChatByOffer} from "../../../fetchoperations/ChatsOperations";
import {Container, TextField} from "@mui/material";
import SendIcon from '@mui/icons-material/Send';
import Button from "@mui/material/Button";
import DeleteIcon from "@mui/icons-material/Delete";
import {useParams} from "react-router-dom";
import Typography from "@mui/material/Typography";

const Chat = () => {
    const {offer_id, chat_id} = useParams();
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState('');
    const [chat, setChat] = useState(undefined);

    const chatWindowRef = useRef(null);
    const socket = useRef(null);

    const username = localStorage.getItem('user');

    useEffect(() => {
        scrollToBottom();
    }, [messages]); // automatic scroll when new message

    useEffect(() => {
        getChat(chat_id).then(r => setChat(r))
    }, [chat_id]);

    useEffect(() => {
        const ws = new WebSocket(`ws://localhost:8000/chats/ws/${offer_id}/${chat?.creator_id}`);
        console.log("Check");
        ws.onopen = (event) => {
            console.log('WebSocket connection opened:', event);
            ws.send(JSON.stringify({type: 'username', user: localStorage.getItem("user")}));
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                const text = JSON.parse(data.text)
                if (text.type === 'message') {
                    const messageWithUsername = {
                        username: text.username,
                        message: text.message,
                        timestamp: data.timestamp
                    };

                    setMessages(messages => messages.concat(messageWithUsername));
                    scrollToBottom();
                }
            } catch {
                console.log('event: ', event);
                console.log('event: ', event.data);
            }
        };

        socket.current = ws;

        return () => {
            console.log('callbackCalled');
            ws.close();
            setMessages([])
        };
    }, [chat?.creator_id, offer_id]);

    const handleChange = (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    }

    const sendMessage = () => {
        if (message && socket.current) {
            const messageData = {
                type: 'message',
                username,
                message,
            };
            setMessages(messages => messages.concat({
                type: 'message_sender',
                message: message,
                username: username,
                timestamp: new Date(Date.now()).toISOString().replace('Z', '').replace('T', ' ').slice(0, -4)
            }));
            socket.current.send(JSON.stringify(messageData));
            setMessage('');
        }
    };

    const clearChat = async () => {
        const chats = await getChats();
        if (chats.length > 0) {
            await deleteChat(await getOwnChatByOffer(offer_id));
            setMessages([]);
        }
    };

    const scrollToBottom = () => {
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
        }
    };

    function transformTimeStamp(timestamp) {
        const [date, time] = timestamp.split(' ');
        return [date, time]
    }


    if (chat === undefined) return <></>
    return (
        <Container maxWidth="sm">
            <div className="chatroom-container">
                <div className="chat-messages" ref={chatWindowRef}>
                    {messages.map((msg, index) => (
                        <div key={index} className={msg.username === username ? "message right" : "message left"}>
                            {/*<strong>{msg.username}:</strong> */}
                            {msg.message}
                            <Typography align={'right'} sx={{fontSize: '1vh'}}>
                                {transformTimeStamp(msg.timestamp)[0] + ' ' + transformTimeStamp(msg.timestamp)[1].slice(0, -3)}
                            </Typography>

                        </div>
                    ))}
                </div>
                <div className="input-container">
                    <div className="input-row">
                        <TextField
                            fullWidth
                            variant="outlined"
                            placeholder="Nachricht eingeben"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            onKeyDown={handleChange}
                        />
                        <Button
                            className='chat-button'
                            variant="contained"
                            color="primary"
                            endIcon={<SendIcon/>}
                            onClick={sendMessage}
                        >
                            Senden
                        </Button>
                    </div>
                    <div className="button-container">
                        <Button
                            className='chat-button'
                            variant="contained"
                            color="error"
                            onClick={clearChat}
                        >
                            <DeleteIcon/>
                        </Button>
                    </div>
                </div>
            </div>
        </Container>
    );
};

export default Chat;
