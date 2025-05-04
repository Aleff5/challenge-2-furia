import React from 'react';

const Hero = () => {
  return (
    <section className="container text-center py-5">
      <div className="mx-auto mb-4 bg-secondary rounded" style={{ width: '150px', height: '150px' }} />
      <h1 className="display-5 fw-bold mb-3">Conecte-se com a FURIA e outros fãs</h1>
      <p className="lead mb-4">
        Bem-vindo à plataforma interativa da FURIA! Aqui, você pode se conectar com a torcida,
        acompanhar eventos emocionantes e acumular pontos por sua participação.
      </p>
      <div className="d-flex justify-content-center gap-3">
        <button className="btn btn-dark px-4">Entrar</button>
        <button className="btn btn-outline-dark px-4">Saiba Mais</button>
      </div>
    </section>
  );
};

export default Hero;
