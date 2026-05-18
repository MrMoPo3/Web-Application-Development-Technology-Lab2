import { NavLink } from 'react-router-dom';

export default function RequireUserNotice() {
  return (
    <section className="empty-state">
      <h2>Потрібен обліковий запис</h2>
      <p>Зареєструйтесь або увійдіть, щоб переглядати персональний профіль.</p>
      <div className="d-flex flex-wrap gap-2">
        <NavLink className="btn btn-dark" to="/register">
          Реєстрація
        </NavLink>
        <NavLink className="btn btn-outline-dark" to="/login">
          Вхід
        </NavLink>
      </div>
    </section>
  );
}
