// used to limit access to specific pages for unauthenticated users

import { Navigate, Outlet } from 'react-router-dom';

export function PrivateRoute({ children }) {
    const isAuthenticated = localStorage.getItem("isLogin");

    if (!isAuthenticated) {
        return <Navigate to="/signin" />;
    }
    return <Outlet />;
}