
import { Box, Typography, Card, FormControl, MenuItem, InputLabel, CardContent, CardActions, Button, Select, Grid, Divider } from "@mui/material";
import React, { useEffect } from "react";
import Cookies from 'universal-cookie';
import record from "../components/record";

const cookies = new Cookies();


export default function RecommendPage() {
    const [type, setType] = React.useState('');
    const [price, setPrice] = React.useState('');
    const [resultList, setResultList] = React.useState([]);
    const [infoList, setInfoList] = React.useState([]);
    const [size, setSize] = React.useState(0);

    const handleTypeChange = (event) => {
        setType(event.target.value);
    }

    const handlePriceChange = (event) => {
        setPrice(event.target.value);
    }

    const getRestaurant = (id) => {
        var requestOptions = {
            method: 'GET',
            redirect: 'follow'
        };

        fetch("http://127.0.0.1:5000/restaurant/id=" + id, requestOptions)
            .then(response => response.json())
            .then(result => { setInfoList(infoList => [...infoList, result]) })
            .catch(error => console.log('error', error));
    }

    useEffect(() => {
        setInfoList([]);
        for (var i = 0; i < resultList.length; i++) {
            getRestaurant(resultList[i]);
        }
        setSize(3);
    }, [resultList])

    const detailClick = (id, index) => {
        record(id, index)
        window.location.href = "/restaurant/" + id;
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        const jsonData = {
            'type': type,
            'price': price
        }

        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("Authorization", "Bearer " + cookies.get('token'));

        var raw = JSON.stringify(jsonData);

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };

        fetch("http://127.0.0.1:5000/restaurant/specify", requestOptions)
            .then(response => response.json())
            .then(result => setResultList(result))
            .catch(error => console.log('error', error));
    }

    const renderResult = () => {
        if (resultList.length === 0) {
            return (
                <Typography component="h1" variant="h5">No Result</Typography>
            );
        } else {
            return (
                <div>
                    <Typography component="h1" variant="h5">為您推薦</Typography>
                    {
                        infoList.slice(0, 1).map((restaurant, index) => (
                            <Card>
                                <CardContent>
                                    <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>{restaurant.id}</Typography>
                                    <Typography variant="h5">{restaurant.name}</Typography>
                                    <Typography sx={{ mb: 1.5 }} color="text.secondary">{restaurant.address}</Typography>
                                    <Typography variant="body2">{restaurant.type}</Typography>
                                </CardContent>
                                <CardActions>
                                    <Button size="small" onClick={function () { detailClick(restaurant.id, index); }}>
                                        show detail
                                    </Button>
                                </CardActions>
                            </Card>
                        ))
                    }
                    <Divider sx={{my: 2}} />
                    {infoList.length > 1 &&
                        <>
                            <Typography component="h1" variant="h5">還可以參考</Typography>
                            <Grid container spacing={3}>
                                {
                                    infoList.slice(1, Math.min(infoList.length, size)).map((restaurant, index) => (
                                        <Grid item key={index}>
                                            <Card>
                                                <CardContent>
                                                    <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>{restaurant.id}</Typography>
                                                    <Typography variant="h5">{restaurant.name}</Typography>
                                                    <Typography sx={{ mb: 1.5 }} color="text.secondary">{restaurant.address}</Typography>
                                                    <Typography variant="body2">{restaurant.type}</Typography>
                                                </CardContent>
                                                <CardActions>
                                                    <Button size="small" onClick={function () { detailClick(restaurant.id, index); }}>
                                                        show detail
                                                    </Button>
                                                </CardActions>
                                            </Card>
                                        </Grid>
                                    ))
                                }
                            </Grid>
                        </>
                    }
                    {
                        size !== infoList.length && <Button variant='contained' color="primary" sx={{ m: 1, minWidth: 120 }} onClick={() => setSize(Math.min(size + 3, infoList.length))}>查看更多</Button>
                    }
                </div>
            );
        }
    };



    return (
        <div>
            <Typography component="h1" variant="h5">Restaurant Recommendation</Typography>
            <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 3 }}>
                <FormControl margin="normal" sx={{ m: 1, minWidth: 120 }}>
                    <InputLabel id='type-label'>Type</InputLabel>
                    <Select labelId='type-label' onChange={handleTypeChange} value={type}>
                        <MenuItem value=''><em>None</em></MenuItem>
                        <MenuItem value='rice'>飯</MenuItem>
                        <MenuItem value='noodle'>麵</MenuItem>
                        <MenuItem value='hotpot'>火鍋</MenuItem>
                        <MenuItem value='breakfast'>早餐</MenuItem>
                    </Select>
                </FormControl>
                <FormControl margin='normal' sx={{ m: 1, minWidth: 120 }}>
                    <InputLabel id='price-label'>Price</InputLabel>
                    <Select labelId='price-label' onChange={handlePriceChange} value={price}>
                        <MenuItem value=''><em>None</em></MenuItem>
                        <MenuItem value={0}>100以下</MenuItem>
                        <MenuItem value={1}>100-150</MenuItem>
                        <MenuItem value={2}>150-200</MenuItem>
                        <MenuItem value={3}>200以上</MenuItem>
                    </Select>
                </FormControl>
                <Button type='submit' variant='contained' color="primary" sx={{ m: 1, minWidth: 120 }}>Submit</Button>
            </Box>

            {renderResult()}

        </div>
    );
}