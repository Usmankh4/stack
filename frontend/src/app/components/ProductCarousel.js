'use client';

import React, { useRef, useEffect, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

const ProductCarousel = ({ 
  products, 
  title, 
  viewAllLink, 
  type = 'default',
  slidesToShow = 4,
  slidesToScroll = 1,
  autoplay = true,
  autoplaySpeed = 3000,
  infinite = true
}) => {
  const sliderRef = useRef(null);
  const [windowWidth, setWindowWidth] = useState(0);
  
  // Responsive settings based on window width
  useEffect(() => {
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };
    
    // Set initial width
    handleResize();
    
    // Add event listener
    window.addEventListener('resize', handleResize);
    
    // Clean up
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  // Dynamically adjust slides to show based on window width
  const getResponsiveSettings = () => {
    return [
      {
        breakpoint: 1200,
        settings: {
          slidesToShow: Math.min(slidesToShow, 3),
          slidesToScroll: 1,
        }
      },
      {
        breakpoint: 992,
        settings: {
          slidesToShow: Math.min(slidesToShow, 2),
          slidesToScroll: 1,
        }
      },
      {
        breakpoint: 576,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        }
      }
    ];
  };

  const settings = {
    dots: true,
    infinite: infinite,
    speed: 500,
    slidesToShow: slidesToShow,
    slidesToScroll: slidesToScroll,
    autoplay: autoplay,
    autoplaySpeed: autoplaySpeed,
    responsive: getResponsiveSettings(),
    nextArrow: <NextArrow />,
    prevArrow: <PrevArrow />
  };

  // Custom arrow components
  function NextArrow(props) {
    const { className, style, onClick } = props;
    return (
      <div
        className={`${className} carousel-arrow carousel-arrow-next`}
        style={{ ...style }}
        onClick={onClick}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M9 18l6-6-6-6" />
        </svg>
      </div>
    );
  }
  
  function PrevArrow(props) {
    const { className, style, onClick } = props;
    return (
      <div
        className={`${className} carousel-arrow carousel-arrow-prev`}
        style={{ ...style }}
        onClick={onClick}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M15 18l-6-6 6-6" />
        </svg>
      </div>
    );
  }

  // Render different card types based on the 'type' prop
  const renderProductCard = (product) => {
    switch (type) {
      case 'flash-deal':
        return (
          <Link key={product.id} href={`/product/${product.type}/${product.slug}`} className="deal-card carousel-card">
            <div className="discount-badge">{product.discount} OFF</div>
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
              <div className="price-container">
                <span className="original-price">${product.originalPrice}</span>
                <span className="sale-price">${product.salePrice}</span>
              </div>
              <div className="timer-container">
                <span className="timer-value">{product.timeLeft} left</span>
              </div>
              <button className="btn btn-primary btn-sm">Add to Cart</button>
            </div>
          </Link>
        );
      
      case 'new-arrival':
        return (
          <Link key={product.id} href={`/product/${product.type}/${product.slug}`} className="product-card new-arrival-card carousel-card">
            <div className="new-badge">NEW</div>
            <div className="card-image">
              <Image 
                src={product.image || '/images/placeholder.png'}
                alt={product.name}
                width={200}
                height={200}
                style={{ objectFit: 'contain' }}
              />
            </div>
            <div className="card-content">
              <h3 className="product-name">{product.name}</h3>
              <div className="price">${product.originalPrice}</div>
              <button className="btn btn-primary btn-sm">Add to Cart</button>
            </div>
          </Link>
        );
      
      case 'best-seller':
        return (
          <Link key={product.id} href={`/product/${product.type}/${product.slug}`} className="product-card best-seller-card carousel-card">
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
              <div className="price">${product.salePrice || product.originalPrice}</div>
              <div className="rating">
                <span className="stars">{'★'.repeat(Math.floor(product.rating))}{'☆'.repeat(5 - Math.floor(product.rating))}</span>
                <span className="review-count">({product.reviewCount})</span>
              </div>
              <button className="btn btn-primary btn-sm">Add to Cart</button>
            </div>
          </Link>
        );
      
      default:
        return (
          <Link key={product.id} href={`/product/${product.type}/${product.slug}`} className="product-card carousel-card">
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
              <div className="price">${product.originalPrice}</div>
              <button className="btn btn-primary btn-sm">Add to Cart</button>
            </div>
          </Link>
        );
    }
  };

  return (
    <section className={`product-carousel-section ${type}-carousel`}>
      <div className="section-header">
        <h2 className="section-title">{title}</h2>
        <Link href={viewAllLink} className="view-all-link">View All</Link>
      </div>
      
      <div className="carousel-container">
        {products && products.length > 0 ? (
          <Slider ref={sliderRef} {...settings}>
            {products.map(product => renderProductCard(product))}
          </Slider>
        ) : (
          <div className="no-products-message">
            <p>No products available at the moment. Check back soon!</p>
          </div>
        )}
      </div>
    </section>
  );
};

export default ProductCarousel;
