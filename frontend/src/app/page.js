import Image from 'next/image';
import Link from 'next/link';
import Header from './components/header';
// Import images from public directory
const bannerImage = "/images/phone.png";
const phoneImages = {
  apple: "/images/15promax.jpg",
  samsung: "/images/samsungultra.jpg",
  google: "/images/Pixel8.png",
  accessories: "/images/Pixel8.png",
  tablets: "/images/Pixel8.png"
};

export const metadata = {
  title: 'ZainWireless - Your Trusted Tech Partner',
  description: 'Professional phone repair services and premium mobile accessories. We specialize in iPhone, Samsung, and other device repairs.',
};

export default function Home() {
  const phoneCards = [
    { id: 'apple', name: 'Apple', link: '/phones/Apple', image: phoneImages.apple },
    { id: 'samsung', name: 'Samsung', link: '/phones/Samsung', image: phoneImages.samsung },
    { id: 'android', name: 'Android', link: '/phones/Android', image: phoneImages.google },
  ];

  const categoryCards = [
    { id: 'accessories', name: 'Accessories', link: '/products/Accessories', image: phoneImages.accessories },
    { id: 'tablets', name: 'Tablets', link: '/phones/Tablet', image: phoneImages.tablets },
  ];

  return (
    <div className="page-container">
      
      <main className="main-content">
        <section className="hero-section">
          <div className="hero-content">
            <div className="hero-text">
              <h1 className="hero-title">REPAIR IS OUR SPECIALTY</h1>
              <div className="hero-buttons">
                <Link href="/products/Accessories">
                  <button className="btn btn-primary">Shop</button>
                </Link>
                <Link href="/repair">
                  <button className="btn btn-outline">Repair</button>
                </Link>
              </div>
            </div>
          </div>
          <div className="hero-image">
            <Image 
              src={bannerImage} 
              alt="Phone Banner" 
              priority
              width={500}
              height={670}
              style={{ objectFit: 'contain' }}
            />
          </div>
        </section>
        
        <section className="products-section">
          <div className="cards-grid">
            {phoneCards.map((card, index) => (
              <Link key={index} href={card.link} className="product-card">
                <div className="card-content">
                  <h2>{card.name}</h2>
                  <button className="view-all-btn">View All</button>
                  <div className="card-image">
                    <Image 
                      src={card.image}
                      alt={`${card.name} product`}
                      width={243}
                      height={243}
                      style={{ objectFit: 'contain' }}
                    />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </section>
        
        <section className="categories-section">
          <div className="category-cards-grid">
            {categoryCards.map((card, index) => (
              <Link key={index} href={card.link} className="category-card">
                <div className="card-content">
                  <h2>{card.name}</h2>
                  <button className="view-all-btn">View All</button>
                  <div className="card-image">
                    <Image 
                      src={card.image}
                      alt={`${card.name} category`}
                      width={243}
                      height={243}
                      style={{ objectFit: 'contain' }}
                    />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </section>
      </main>
      
      
    </div>
  );
}