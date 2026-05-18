import { useState } from 'react';
import { LogIn } from 'lucide-react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import PageHeader from '../components/PageHeader.jsx';
import { loginUser } from '../store/authSlice.js';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const users = useSelector((state) => state.auth.users);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  function handleSubmit(event) {
    event.preventDefault();
    const normalizedEmail = email.trim().toLowerCase();
    const user = users.find((item) => item.email === normalizedEmail && item.password === password);

    if (!user) {
      setError('Користувача з таким email і паролем не знайдено.');
      return;
    }

    dispatch(loginUser({ email: normalizedEmail }));
    navigate('/profile');
  }

  return (
    <section className="container page-grid auth-page">
      <PageHeader eyebrow="Авторизація" title="Вхід до сайту">
        Увійдіть до створеного профілю, щоб продовжити роботу з даними.
      </PageHeader>

      <form className="surface-form" onSubmit={handleSubmit}>
        {error ? <div className="alert alert-danger">{error}</div> : null}

        <label className="form-label" htmlFor="loginEmail">
          Email
        </label>
        <input
          className="form-control"
          id="loginEmail"
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          placeholder="student@example.com"
        />

        <label className="form-label" htmlFor="loginPassword">
          Пароль
        </label>
        <input
          className="form-control"
          id="loginPassword"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="Ваш пароль"
        />

        <button className="btn btn-dark btn-lg w-100" type="submit">
          <LogIn size={18} aria-hidden="true" />
          Увійти
        </button>
      </form>
    </section>
  );
}
