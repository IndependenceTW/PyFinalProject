import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Cookies from 'universal-cookie';
import FileInput from '../components/FileInput';
import Iconify from '../components/Iconify';

const theme = createTheme();
const cookies = new Cookies();

export default function NewMenuPage() {
    const [form, setForm] = React.useState({});

    const handleSubmit = (event) => {
    };

    const handleOCR = () => {
        if (form) {
            var myHeaders = new Headers();
            myHeaders.append("Authorization", "Bearer " + cookies.get("token"));
            
            console.log(form);

            var requestOptions = {
                method: 'POST',
                headers: myHeaders,
                body: form,
                redirect: 'follow'
            };

            fetch("127.0.0.1:5000/restaurant/menu/ocr", requestOptions)
                .then(response => response.text())
                .then(result => console.log(result))
                .catch(error => console.log('error', error));

        }
    }

    return (
        <ThemeProvider theme={theme}>
            <Container component="main">
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
                        New Menu
                    </Typography>
                    <FileInput setForm={setForm}/>
                    <Button variant="contained" component="span" color="info" startIcon={<Iconify icon="material-symbols:send-rounded"/>} onClick={() => handleOCR()}>
                        OCR start
                    </Button>
                    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                        <TextField
                            margin="normal"
                            multiline
                            fullWidth
                            placeholder='格式: "菜名" "價格"\n'
                            name="menu"
                            label="Menu"
                            id="menu"
                        />
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