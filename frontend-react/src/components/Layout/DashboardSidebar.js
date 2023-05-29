import PropTypes from 'prop-types';
import { React, useEffect, useState } from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
// material
import { styled } from '@mui/material/styles';
import { Box, Link, Drawer, Typography, Avatar, Stack, Button } from '@mui/material';
// mock
// hooks
import useResponsive from './useResponsive';
// components
import Logo from './Logo';
import Scrollbar from './Scrollbar'
import NavSection from './NavSection';
//
import navConfig from './NavConfig';
import Cookies from 'universal-cookie';
// ----------------------------------------------------------------------

const DRAWER_WIDTH = 280;


const RootStyle = styled('div')(({ theme }) => ({
  [theme.breakpoints.up('lg')]: {
    flexShrink: 0,
    width: DRAWER_WIDTH,
    height: '100%',
  },
}));

const AccountStyle = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(2, 2.5),
  borderRadius: Number(theme.shape.borderRadius) * 1.5,
  backgroundColor: theme.palette.grey[500_12],
}));

// ----------------------------------------------------------------------

DashboardSidebar.propTypes = {
  isOpenSidebar: PropTypes.bool,
  onCloseSidebar: PropTypes.func,
};


export default function DashboardSidebar({ isOpenSidebar, onCloseSidebar }) {
  const { pathname } = useLocation();
  const isDesktop = useResponsive('up', 'lg');
  const cookies = new Cookies();
  const token = cookies.get('token');
  const username = cookies.get('username');

  useEffect(() => {
    if (isOpenSidebar) {
      onCloseSidebar();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname]);

  const handleLogout = () => {
    cookies.remove('token');
    window.location.reload();
  }

  const renderContent = (
    <Scrollbar
      sx={{
        height: 1,
        '& .simplebar-content': { height: 1, display: 'flex', flexDirection: 'column' },
      }}
    >
      <Box sx={{ px: 2.5, py: 3, display: 'inline-flex' }}>
        <Logo />
      </Box>
      
      {!token && (
        <Box sx={{ px: 2.5, py: 3, display: 'inline-flex' }}>
          <Button href="/login" variant="contained">
            Login
          </Button>
        </Box>
      )}

      {
        token && (
          <Box sx={{ px: 2.5, py: 3, display: 'inline-flex' }}>
            <Button variant="contained" onClick={handleLogout} color="error">
              Logout
            </Button>
          </Box>
        )
      }

      <NavSection navConfig={navConfig} />
    </Scrollbar>
  );

  return (
    <RootStyle>
      {/* mobile */}
      {!isDesktop && (
          <Drawer
            open={isOpenSidebar}
            onClose={onCloseSidebar}
            PaperProps={{
              sx: { width: DRAWER_WIDTH },
            }}
          >
            {renderContent}
          </Drawer>
      )}
      {/* <Box justify="flex-end">
        {username ? <Link href="/signin" onClick={handleLogout} variant="body2">Logout</Link> : <Link href="/signin" variant="body2">Login</Link>}
      </Box> */}

      {isDesktop && (
        <Drawer
          open
          variant="persistent"
          PaperProps={{
            sx: {
              width: DRAWER_WIDTH,
              bgcolor: 'background.default',
              borderRightStyle: 'dashed',
            },
          }}
        >
          {renderContent}
        </Drawer>
      )}
    </RootStyle>
  );
}
