import { colors } from '@material-ui/core';

const white = '#FFFFFF';
const black = '#000000';


export default {
  black,
  white,
  primary: {
    contrastText: white,
    dark: colors.teal[900],
    main: colors.teal[500],
    light: colors.teal[100],
  },
  secondary: {
    contrastText: white,
    dark: colors.grey[900],
    main: colors.grey['A400'],
    light: colors.grey['A400']
  },
  success: {
    contrastText: white,
    dark: colors.green[900],
    main: colors.green[600],
    light: colors.green[400]
  },
  info: {
    contrastText: white,
    dark: colors.blue[900],
    main: colors.blue[600],
    light: colors.blue[400]
  },
  warning: {
    contrastText: white,
    dark: colors.orange[900],
    main: colors.orange[600],
    light: colors.orange[400]
  },
  error: {
    contrastText: white,
    dark: colors.red[900],
    main: colors.red[600],
    light: colors.red[400]
  },
  text: {
    primary: colors.blueGrey[900],
    secondary: colors.blueGrey[600],
    link: colors.blue[600]
  },
  text2: {
    primary: colors.white
  },
  background: {
    default: '#F4F6F8',
    paper: white
  },
  icon: colors.blueGrey[600],
  divider: colors.grey[200]
};
