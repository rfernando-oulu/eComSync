import React, { useState, useEffect } from 'react';
import ProductList from './ProductList';
import AddProduct from './AddProduct';
import axios from 'axios';

const ProductPage = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/product');
      setProducts(response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const addProduct = async (newProduct) => {
    try {
      await axios.post('http://localhost:5000/api/product', newProduct);
      setProducts([...products, newProduct]);
    } catch (error) {
      console.error('Error adding product:', error);
    }
  };

  return (
    <div>
      <ProductList products={products} />
      <AddProduct onAddProduct={addProduct} />
    </div>
  );
};

export default ProductPage;
