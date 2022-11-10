import { createTheme } from "@mui/material/styles";

const theme = createTheme({
    palette: {
        primary: {
            main: '#ffcd02',
            light: '#ffd734',
            dark: '#b28f01',
        },
        secondary: {
            main: '#33319f',
            light: '#23226f',
            dark: '#5b5ab2',
        },
    },
    components: {
        MuiInputLabel: {
            styleOverrides: {
                root: {
                    '&.Mui-focused': {
                        color: '#b28f01'
                    },
                },
            },
        },
    },
});

export default theme;
