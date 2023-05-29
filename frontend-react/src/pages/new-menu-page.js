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
import { useParams } from 'react-router-dom';

const theme = createTheme();
const cookies = new Cookies();

export default function NewMenuPage() {
    const { id } = useParams();
    const [form, setForm] = React.useState({});
    const [input, setInput] = React.useState("");

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        const raw_data = data.get('menu');
        const menu = raw_data.split('\n');
        var menu_json = [];
        for (var i = 0; i < menu.length; i++) {
            var item = menu[i].split(' ');
            if (item.length === 2) {
                menu_json.push({
                    "name": item[0],
                    "price": item[1]
                })
            }
        }

        var myHeaders = new Headers();
        myHeaders.append("Authorization", "Bearer " + cookies.get("token"));
        myHeaders.append("Content-Type", "application/json");

        var raw = JSON.stringify(menu_json);

        const requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };

        console.log(raw)
        console.log(requestOptions)

        fetch("http://127.0.0.1:5000/restaurant/id="+id+"/menu", requestOptions)
            .then(response => {
                if (response.status === 200) {
                    alert("Create menu success!");
                    window.location.href = "/restaurant/" + id
                }
            })
            .catch(error => console.log('error', error));
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

            fetch("http://127.0.0.1:5000/restaurant/menu/ocr", requestOptions)
                .then(response => response.text())
                .then(result => {
                    var text = unescape(result.replace(/\\u/g, '%u'));
                    setInput(text)
                })
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
                    <FileInput setForm={setForm} />
                    <Button variant="contained" component="span" color="info" startIcon={<Iconify icon="material-symbols:send-rounded" />} onClick={() => handleOCR()}>
                        OCR start
                    </Button>
                    {
                        input && (
                            <Box mt={2} textAlign="center">
                                <Typography component="h1" variant="h5">
                                    Result: {input}
                                </Typography>
                            </Box>
                        )
                    }
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