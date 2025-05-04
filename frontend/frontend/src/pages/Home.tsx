import Navbar from '../components/Home/Navbar';
import Hero from '../components/Home/Hero';
import CTASection from '../components/Home/CTASection';
import FeaturedCards from '../components/Home/FeaturedCards';
import Footer from '../components/Home/Footer';

const Home = () => {
  return (
    <>
      <Navbar />
      <Hero />
      <CTASection />
      <FeaturedCards />
      <Footer />
    </>
  );
};

export default Home;
