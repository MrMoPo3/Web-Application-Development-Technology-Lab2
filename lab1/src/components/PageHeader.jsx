export default function PageHeader({ eyebrow, title, children }) {
  return (
    <header className="page-header">
      <span className="eyebrow">{eyebrow}</span>
      <h1>{title}</h1>
      {children ? <p>{children}</p> : null}
    </header>
  );
}
