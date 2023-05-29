import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Card, CardContent, Container, Grid, Typography, Stack, Button, Divider} from "@mui/material";
import Page from "../components/Page";
import Iconify from "../components/Iconify";
import { Link as RouterLink } from "react-router-dom";

const getRestaurant = async (id) => {
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    return fetch("http://127.0.0.1:5000/restaurant/id=" + id, requestOptions)
        .then(response => response.json())
        .catch(error => console.log('error', error));
}

const getMenu = async (id) => {
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    return fetch("http://127.0.0.1:5000/restaurant/id=1PPekYsTDiAYSkp4H55H/menu", requestOptions)
        .then(response => response.json())
        .catch(error => console.log('error', error));
}


export default function RestaurantDetailPage() {
    const { id } = useParams();

    const [restaurant, setRestaurant] = useState(null);
    const [menu, setMenu] = useState(null);

    const fetchRestaurant = async () => {
        const r = await getRestaurant(id);
        setRestaurant(r);
    }

    const fetchMenu = async () => {
        const m = await getMenu(id);
        setMenu(m);
    }

    useEffect(() => {
        fetchRestaurant();
        fetchMenu();
    }, []);

    return (
        <Page title="detail">
            <Container>
                <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
                    <Typography variant="h3" gutterBottom>
                        {restaurant && restaurant.name}
                    </Typography>
                    <Button variant="contained" component={RouterLink} to="/restaurant/:id/addmenu" startIcon={<Iconify icon="eva:plus-fill" />}>
                        Add Menu
                    </Button>
                </Stack>
                {restaurant && restaurant.mean_price === 0 && <Typography variant="subtitle1">價格範圍：100元以下</Typography>}
                {restaurant && restaurant.mean_price === 1 && <Typography variant="subtitle1">價格範圍：100~150元</Typography>}
                {restaurant && restaurant.mean_price === 2 && <Typography variant="subtitle1">價格範圍：150~200元</Typography>}
                {restaurant && restaurant.mean_price === 3 && <Typography variant="subtitle1">價格範圍：200元以上</Typography>}
                <Typography variant="subtitle1">餐廳地址：{restaurant && restaurant.address}</Typography>
                <Typography variant="subtitle1">餐廳類型：{restaurant && restaurant?.type}</Typography>
                <Divider sx={{my: 2}} />
                <Grid container spacing={3}>
                {menu && menu.map((food, index) => (
                    <Grid item key = {index}>
                        <Card>
                            <CardContent>
                                <Typography gutterBottom variant="h5" component="div">{food.name}</Typography>
                                <Typography variant="body2" color="text.secondary">價格: {food.type}</Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
                </Grid>
            </Container>
        </Page>
    );
}