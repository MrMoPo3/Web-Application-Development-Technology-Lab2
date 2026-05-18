import { LogOut, PieChart, UserRound } from 'lucide-react';
import { NavLink, Outlet } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { logoutUser } from '../store/authSlice.js';

const navItems = [
  { to: '/polls', label: 'Опитування' },
  { to: '/about', label: 'Про додаток' },
  { to: '/profile', label: 'Профіль' },
];

export default function Layout() {
  const dispatch = useDispatch();
  const currentUser = useSelector((state) =>
    state.auth.users.find((user) => user.email === state.auth.currentUserEmail),
  );

  return (
    <div className="app-shell">
      <nav className="navbar navbar-expand-lg sticky-top app-navbar">
        <div className="container">
          <NavLink className="navbar-brand d-flex align-items-center gap-2" to="/polls">
            <span className="brand-mark" aria-hidden="true">
              <PieChart size={22} />
            </span>
            PollCraft
          </NavLink>

          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#mainNavigation"
            aria-controls="mainNavigation"
            aria-expanded="false"
            aria-label="Перемкнути навігацію"
          >
            <span className="navbar-toggler-icon" />
          </button>

          <div className="collapse navbar-collapse" id="mainNavigation">
            <div className="navbar-nav mx-lg-auto">
              {navItems.map((item) => (
                <NavLink key={item.to} className="nav-link" to={item.to}>
                  {item.label}
                </NavLink>
              ))}
            </div>

            <div className="navbar-nav align-items-lg-center gap-lg-2">
              {currentUser ? (
                <>
                  <span className="user-chip">
                    <UserRound size={16} />
                    {currentUser.name}
                  </span>
                  <button className="btn btn-outline-dark btn-sm" onClick={() => dispatch(logoutUser())}>
                    <LogOut size={16} aria-hidden="true" />
                    Вийти
                  </button>
                </>
              ) : (
                <>
                  <NavLink className="btn btn-outline-dark btn-sm" to="/login">
                    Вхід
                  </NavLink>
                  <NavLink className="btn btn-dark btn-sm" to="/register">
                    Реєстрація
                  </NavLink>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
