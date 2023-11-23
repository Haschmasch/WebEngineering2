import {ListItem, ListItemIcon, ListItemText} from "@mui/material";

export default function FollowingListRow(props) {
    if (props === undefined) {
        return {}
    }
    console.log(props);
    const offer = props.following.related_offer;
    return (
        <ListItem>
            <ListItemIcon>
                <img src={offer.primary_image} alt={offer.title}/>
            </ListItemIcon>
            <ListItemText>
                {offer.title}
            </ListItemText>
            <ListItemText>
                {offer.price + offer.currency}
            </ListItemText>
        </ListItem>
    )

}