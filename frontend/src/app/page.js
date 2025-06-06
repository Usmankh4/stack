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
  title: 'Mobile Repair & Accessories - Your Trusted Tech Partner',
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

  // Mock data for promotional sections (will be replaced with backend data later)
  const flashDeals = [
    { id: 1, name: 'iPhone 15 Pro', originalPrice: 999, salePrice: 899, image: phoneImages.apple, discount: '10%', timeLeft: '5h 23m' },
    { id: 2, name: 'Samsung S24 Ultra', originalPrice: 1199, salePrice: 999, image: phoneImages.samsung, discount: '17%', timeLeft: '5h 23m' },
    { id: 3, name: 'Google Pixel 8', originalPrice: 799, salePrice: 699, image: phoneImages.google, discount: '12%', timeLeft: '5h 23m' },
  ];

  const newArrivals = [
    { id: 1, name: 'iPhone 15 Pro Max', price: 1099, image: phoneImages.apple, isNew: true },
    { id: 2, name: 'Samsung Galaxy Buds', price: 149, image: phoneImages.accessories, isNew: true },
    { id: 3, name: 'Google Pixel Tablet', price: 499, image: phoneImages.tablets, isNew: true },
  ];

  const bestSellers = [
    { id: 1, name: 'iPhone 14 Pro', price: 899, image: phoneImages.apple, rating: 4.8, reviewCount: 245 },
    { id: 2, name: 'Samsung S23', price: 799, image: phoneImages.samsung, rating: 4.7, reviewCount: 189 },
    { id: 3, name: 'Phone Charging Stand', price: 29.99, image: phoneImages.accessories, rating: 4.9, reviewCount: 412 },
  ];

  const bundleDeals = [
    { 
      id: 1, 
      name: 'iPhone Essentials Bundle', 
      items: ['iPhone 15', 'MagSafe Charger', 'Silicone Case', 'Screen Protector'],
      originalPrice: 1156, 
      bundlePrice: 999,
      image: phoneImages.apple 
    },
    { 
      id: 2, 
      name: 'Samsung Ultimate Pack', 
      items: ['Samsung S24', 'Wireless Charger', 'Galaxy Buds', 'Clear Case'],
      originalPrice: 1356, 
      bundlePrice: 1199,
      image: phoneImages.samsung 
    },
  ];

  const testimonials = [
    { id: 1, name: 'John D.', rating: 5, comment: 'Excellent service and quality products. My phone was repaired in under an hour!', date: '2 weeks ago' },
    { id: 2, name: 'Sarah M.', rating: 5, comment: 'The accessories I bought were exactly as described and arrived quickly. Will shop again!', date: '1 month ago' },
    { id: 3, name: 'Michael T.', rating: 4, comment: 'Great selection of phones and very knowledgeable staff. Highly recommend.', date: '3 weeks ago' },
  ];

  const promotions = [
    { id: 1, title: 'SUMMER SALE', subtitle: 'Up to 30% off select accessories', buttonText: 'Shop Now', link: '/sale' },
    { id: 2, title: 'FREE SCREEN PROTECTOR', subtitle: 'With any phone purchase', buttonText: 'View Phones', link: '/phones' },
    { id: 3, title: 'TRADE-IN OFFER', subtitle: 'Get up to $500 for your old device', buttonText: 'Learn More', link: '/trade-in' },
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
        
        {/* Featured Promotions Banner */}
        <section className="promotions-banner">
          <div className="promo-slider">
            {promotions.map((promo, index) => (
              <div key={promo.id} className={`promo-slide ${index === 0 ? 'active' : ''}`}>
                <div className="promo-content">
                  <h2 className="promo-title">{promo.title}</h2>
                  <p className="promo-subtitle">{promo.subtitle}</p>
                  <Link href={promo.link}>
                    <button className="btn btn-primary">{promo.buttonText}</button>
                  </Link>
                </div>
              </div>
            ))}
            <div className="promo-indicators">
              {promotions.map((_, index) => (
                <span key={index} className={`indicator ${index === 0 ? 'active' : ''}`}></span>
              ))}
            </div>
          </div>
        </section>
        
        {/* Flash Deals Section */}
        <section className="flash-deals-section">
          <div className="section-header">
            <h2 className="section-title">Flash Deals</h2>
            <div className="countdown-timer">
              <span className="timer-label">Ends in:</span>
              <span className="timer-value">05:23:47</span>
            </div>
          </div>
          <div className="deals-slider">
            {flashDeals.map((deal) => (
              <Link key={deal.id} href={`/product/${deal.id}`} className="deal-card">
                <div className="discount-badge">{deal.discount} OFF</div>
                <div className="card-image">
                  <Image 
                    src={deal.image}
                    alt={deal.name}
                    width={200}
                    height={200}
                    style={{ objectFit: 'contain' }}
                  />
                </div>
                <div className="card-content">
                  <h3 className="product-name">{deal.name}</h3>
                  <div className="price-container">
                    <span className="original-price">${deal.originalPrice}</span>
                    <span className="sale-price">${deal.salePrice}</span>
                  </div>
                  <button className="btn btn-primary btn-sm">Add to Cart</button>
                </div>
              </Link>
            ))}
          </div>
        </section>
        
        <section className="new-arrivals-section">
          <div className="section-header">
            <h2 className="section-title">Just Arrived</h2>
            <Link href="/new-arrivals" className="view-all-link">View All</Link>
          </div>
          <div className="new-arrivals-grid">
            {newArrivals.map((product) => (
              <Link key={product.id} href={`/product/${product.id}`} className="product-card new-arrival-card">
                {product.isNew && <div className="new-badge">NEW</div>}
                <div className="card-image">
                  <Image 
                    src={product.image}
                    alt={product.name}
                    width={200}
                    height={200}
                    style={{ objectFit: 'contain' }}
                  />
                </div>
                <div className="card-content">
                  <h3 className="product-name">{product.name}</h3>
                  <div className="price">${product.price}</div>
                  <button className="btn btn-primary btn-sm">Add to Cart</button>
                </div>
              </Link>
            ))}
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

        <section className="best-sellers-section">
          <div className="section-header">
            <h2 className="section-title">Customer Favorites</h2>
            <Link href="/best-sellers" className="view-all-link">View All</Link>
          </div>
          <div className="best-sellers-grid">
            {bestSellers.map((product) => (
              <Link key={product.id} href={`/product/${product.id}`} className="product-card best-seller-card">
                <div className="bestseller-badge">Best Seller</div>
                <div className="card-image">
                  <Image 
                    src={product.image}
                    alt={product.name}
                    width={200}
                    height={200}
                    style={{ objectFit: 'contain' }}
                  />
                </div>
                <div className="card-content">
                  <h3 className="product-name">{product.name}</h3>
                  <div className="price">${product.price}</div>
                  <div className="rating">
                    <span className="stars">{'★'.repeat(Math.floor(product.rating))}{'☆'.repeat(5 - Math.floor(product.rating))}</span>
                    <span className="review-count">({product.reviewCount})</span>
                  </div>
                  <button className="btn btn-primary btn-sm">Add to Cart</button>
                </div>
              </Link>
            ))}
          </div>
        </section>
        
        
        <section className="bundle-deals-section">
          <div className="section-header">
            <h2 className="section-title">Save with Bundles</h2>
            <Link href="/bundles" className="view-all-link">View All</Link>
          </div>
          <div className="bundles-grid">
            {bundleDeals.map((bundle) => (
              <Link key={bundle.id} href={`/bundle/${bundle.id}`} className="bundle-card">
                <div className="savings-badge">Save ${(bundle.originalPrice - bundle.bundlePrice).toFixed(2)}</div>
                <div className="card-image">
                  <Image 
                    src={bundle.image}
                    alt={bundle.name}
                    width={200}
                    height={200}
                    style={{ objectFit: 'contain' }}
                  />
                </div>
                <div className="card-content">
                  <h3 className="bundle-name">{bundle.name}</h3>
                  <ul className="bundle-items">
                    {bundle.items.map((item, i) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                  <div className="price-container">
                    <span className="original-price">${bundle.originalPrice}</span>
                    <span className="bundle-price">${bundle.bundlePrice}</span>
                  </div>
                  <button className="btn btn-primary">Add Bundle to Cart</button>
                </div>
              </Link>
            ))}
          </div>
        </section>
        
        <section className="testimonials-section">
          <h2 className="section-title">What Our Customers Say</h2>
          <div className="testimonials-slider">
            {testimonials.map((testimonial) => (
              <div key={testimonial.id} className="testimonial-card">
                <div className="testimonial-rating">
                  {'★'.repeat(testimonial.rating)}{'☆'.repeat(5 - testimonial.rating)}
                </div>
                <p className="testimonial-text">"{testimonial.comment}"</p>
                <div className="testimonial-author">
                  <span className="author-name">{testimonial.name}</span>
                  <span className="testimonial-date">{testimonial.date}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
        
        <section className="newsletter-section">
          <div className="newsletter-content">
            <h2 className="newsletter-title">Get 10% Off Your First Order</h2>
            <p className="newsletter-text">Subscribe to our newsletter for exclusive deals and updates</p>
            <form className="newsletter-form">
              <input type="email" placeholder="Your email address" className="newsletter-input" required />
              <button type="submit" className="btn btn-primary">Subscribe</button>
            </form>
          </div>
        </section>
      </main>
      
      
    </div>
  );
}