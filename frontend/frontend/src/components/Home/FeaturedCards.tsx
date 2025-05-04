import React from 'react';

const cards = [
  {
    title: 'Medium length section heading goes here',
    text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse varius enim.',
  },
  {
    title: 'Medium length section heading goes here',
    text: 'Duis cursus, mi quis viverra ornare, eros dolor interdum nulla, ut commodo diam libero vitae erat.',
  },
  {
    title: 'Medium length section heading goes here',
    text: 'Aenean faucibus nibh et justo cursus id rutrum lorem imperdiet. Nunc ut sem vitae risus tristique posuere.',
  },
];

const FeaturedCards = () => {
  return (
    <section className="container py-5">
      <div className="row g-4">
        {cards.map((card, index) => (
          <div key={index} className="col-md-4">
            <div className="card h-100 text-center shadow-sm">
              <div className="bg-secondary rounded-top" style={{ height: '150px' }} />
              <div className="card-body">
                <h5 className="card-title">{card.title}</h5>
                <p className="card-text text-muted">{card.text}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default FeaturedCards;
