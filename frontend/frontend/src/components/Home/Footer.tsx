import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-light text-center text-muted py-5">
      <div className="mb-3">
        <strong className="text-dark">Logo</strong>
      </div>
      <div className="d-flex justify-content-center flex-wrap gap-3 mb-3 small">
        <a href="#" className="text-decoration-none text-muted">Link Um</a>
        <a href="#" className="text-decoration-none text-muted">Link Dois</a>
        <a href="#" className="text-decoration-none text-muted">Link Três</a>
        <a href="#" className="text-decoration-none text-muted">Link Quatro</a>
        <a href="#" className="text-decoration-none text-muted">Link Cinco</a>
      </div>
      <p className="small mb-0">&copy; 2025 Know Your Fan. Todos os direitos reservados.</p>
    </footer>
  );
};

export default Footer;
