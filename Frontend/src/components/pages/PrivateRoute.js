/* used to limit access to specific pages for unauthenticated users */

import { Navigate, Outlet } from 'react-router-dom';
import {isLoggedIn} from "../utils/StorageInterface";

export function PrivateRoute() {
    if (!isLoggedIn()) {
        return <Navigate to="/signin" />;
    }
    return <Outlet />;
}