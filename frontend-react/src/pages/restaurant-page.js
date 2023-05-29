import { useEffect, useState } from "react";
import Page from "../components/Page";
import { Container, Stack, Typography, Button, Grid, Card, CardContent, CardActions} from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import Iconify from "../components/Iconify";

export default function RestaurantsPage() {
    const [restaurants, setRestaurants] = useState([]);

    async function fetchRestaurants() {
        const response = await fetch('http://127.0.0.1:5000/restaurant');
        const data = await response.json();
        setRestaurants(data);
    }

    const detailClick = (id) => {
        console.log('hello');
        
        window.location.href = "/restaurant/"+id;
    }

    useEffect(() => {
        fetchRestaurants();
    }, []);
    


    return (
        <Page title="Restaurant list">
            <Container>
                <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
                    <Typography variant="h4" gutterBottom>
                        Restaurant list
                    </Typography>
                    <Button variant="contained" component={RouterLink} to="/restaurant/create" startIcon={<Iconify icon="eva:plus-fill" />}>
                        New Restaurant
                    </Button>
                </Stack>

                <Grid container spacing={3}>
                        {
                            restaurants.map((restaurant, index) => (
                                <Grid item key={index}>
                                    <Card>
                                        <CardContent>
                                            <Typography sx={{fontSize: 14}} color="text.secondary" gutterBottom>{restaurant.id}</Typography>
                                            <Typography variant="h5">{restaurant.name}</Typography>
                                            <Typography sx={{mb: 1.5}} color="text.secondary">{restaurant.address}</Typography>
                                            <Typography variant="body2">{restaurant.type}</Typography>
                                        </CardContent>
                                        <CardActions>
                                            <Button size="small" onClick={function() {detailClick(restaurant.id);}}>
                                                show detail
                                            </Button>
                                        </CardActions>
                                    </Card>
                                </Grid>
                            ))
                        }
                    </Grid>
            </Container>
        </Page>
    );
}