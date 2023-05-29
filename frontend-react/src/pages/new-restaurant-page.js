import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import { FormControl, InputLabel, MenuItem, Select } from '@mui/material';
// import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
// import { getCookie, setCookie } from '../../global/api/cookie';
import { useNavigate } from "react-router-dom";
import Cookies from 'universal-cookie';
// import GetTwilioToken from '../../global/api/getTwilioToken';




const theme = createTheme();

export default function NewRestaurant() {
    const [type, setType] = React.useState('');
    const [price, setPrice] = React.useState('');
    const cookies = new Cookies();
    const navigate = useNavigate();

    const handleTypeChange = (event) => {
        setType(event.target.value);
    }

    const handlePriceChange = (event) => {
        setPrice(event.target.value);
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        const jsonData = {
            name: data.get('name'),
            address: data.get('address'),
            type: type,
            price: price
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

        fetch("http://127.0.0.1:5000/restaurant/", requestOptions)
            .then(response => {
                if (response.status === 201) {
                    alert("Create Success!");
                    navigate('/restaurant', { replace: true });
                } 
                else if (response.status === 422) {
                    alert('please login again!')
                    navigate('/login', { replace: true });
                }
                else if (response.status === 401) {
                    alert("Unauthorized! Please Login Again!")
                    cookies.remove('token');
                    navigate('/login', { replace: true });
                }
                else {
                    alert("Create Fail with unknown problem!");
                    console.log(response.status);
                }
            })
    };

    return (
        <ThemeProvider theme={theme}>
            <Container component="main" maxWidth="xs">
                <CssBaseline />
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Typography component="h1" variant="h5">
                        New Restaurant
                    </Typography>
                    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="name"
                            label="Restaurant Name"
                            name="name"
                            autoFocus
                        />
                        <TextField
                            margin='normal'
                            required
                            fullWidth
                            id="address"
                            label="Restaurant Address"
                            name="address"
                            autoFocus
                        />
                        <FormControl fullWidth required margin='normal'>
                            <InputLabel id='type-label'>Type</InputLabel>
                            <Select labelId='type-label' onChange={handleTypeChange}>
                                <MenuItem value='rice'>飯</MenuItem>
                                <MenuItem value='noodle'>麵</MenuItem>
                                <MenuItem value='hotpot'>火鍋</MenuItem>
                                <MenuItem value='breakfast'>早餐</MenuItem>
                            </Select>
                        </FormControl>
                        <FormControl fullWidth required margin='normal'>
                            <InputLabel id='price-label'>Price</InputLabel>
                            <Select labelId='price-label' onChange={handlePriceChange}>
                                <MenuItem value={0}>100以下</MenuItem>
                                <MenuItem value={1}>100-150</MenuItem>
                                <MenuItem value={2}>150-200</MenuItem>
                                <MenuItem value={3}>200以上</MenuItem>
                            </Select>
                        </FormControl>


                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Create!
                        </Button>
                    </Box>
                </Box>
            </Container>
        </ThemeProvider>
    );
}