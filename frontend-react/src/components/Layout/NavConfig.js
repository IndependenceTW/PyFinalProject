// component
import Iconify from "../Iconify";

// ----------------------------------------------------------------------

const getIcon = (name) => <Iconify icon={name} width={22} height={22} />;

const navConfig = [
  {
    title: 'Restaurant list',
    path: '/restaurant',
    icon: getIcon('material-symbols:restaurant'),
  },
  {
    title: 'Recommendation',
    path: '/recommend',
    icon: getIcon('mdi:food'),
  }

  // {
  //   title: 'login',
  //   path: '/login',
  //   icon: getIcon('eva:lock-fill'),
  // },
];

export default navConfig;
