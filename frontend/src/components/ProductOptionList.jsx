import React, { useState, useEffect } from 'react';
import { fetchManufacturersFunction } from './api';
import axios from 'axios';

const ProductList = () => {
  const [products, setProducts] = useState([]);

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [sku, setSku] = useState('');
  const [manufacturers, setManufacturers] = useState([]);
  const [manufacturerId, setManufacturerId] = useState("");
  const [quantity, setQuantity] = useState('');
  const [image, setImage] = useState('');
  const [price, setPrice] = useState('');
  const [width, setWidth] = useState('');
  const [options, setOptions] = useState('');
  const [date_added, setDateAdded] = useState('');

  const [editingId, setEditingId] = useState(null);

  const [name_update, setUpdateName] = useState('');
  const [description_update, setUpdateDescription] = useState('');
  const [sku_update, setUpdateSku] = useState('');
  const [quantity_update, setUpdateQuantity] = useState('');
  const [image_update, setUpdateImage] = useState('');
  const [price_update, setUpdatePrice] = useState('');
  const [width_update, setUpdateWidth] = useState('');
  const [date_added_update, setUpdateDateAdded] = useState('');

  useEffect(() => {
    fetchProducts();
    setDateAdded(getCurrentDateTime());
  }, []);
  
  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/product/`, {
        headers: { 'access-key': import.meta.env.VITE_ACCESS_KEY }
      });
      const productsWithDetails = await Promise.all(response.data.products.map(async product => {
        const productDetailResponse = await axios.get(`${import.meta.env.VITE_API_URL}${product['@controls'].self.href}`, {
          headers: { 'access-key': import.meta.env.VITE_ACCESS_KEY }
        });
        return productDetailResponse.data;
      }));
      setProducts(productsWithDetails);


      setManufacturers(await fetchManufacturersFunction());
      

    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const deleteProduct = async (id) => { 
    try {
      await axios.delete(`${import.meta.env.VITE_API_URL}/api/product/${id}`);
      setProducts(products.filter((product) => product.id !== id));
      alert(`Product with ID: ${id} deleted successfully!`);
      fetchProducts();
    } catch (error) {
      console.error('Error deleting product:', error);
    }
  };

  const getCurrentDateTime = () => {
    const date = new Date();
    const yyyy = date.getUTCFullYear();
    const mm = String(date.getUTCMonth() + 1).padStart(2, '0');
    const dd = String(date.getUTCDate()).padStart(2, '0');
    const hh = String(date.getUTCHours()).padStart(2, '0');
    const min = String(date.getUTCMinutes()).padStart(2, '0');
    const sec = String(date.getUTCSeconds()).padStart(2, '0');
  
    const formattedDate = `${yyyy}-${mm}-${dd}T${hh}:${min}:${sec}+00:00`;
    return String(formattedDate);
  };

  const addProduct = async (e) => {
    e.preventDefault();

    try { 
      await axios.post(`${import.meta.env.VITE_API_URL}/api/product/`, { // Replace with your Flask API endpoint
        name,
        description,
        sku,
        manufacturerId,
        quantity,
        image,
        price,
        width,
        date_added

      });

      setName('');
      setDescription('');
      setSku('');
      setManufacturerId('');
      setQuantity('');
      setImage('');
      setPrice('');
      setWidth('');
      alert('Product added successfully!');
      fetchProducts();
    } catch (error) {
      if (error.response) {
        console.error('Error:', error.response);
        alert(error.response.data);
      } 
      console.error('Error adding product:', error);
    }
  };

  const startUpdate = (product) => {
    setEditingId(product.id);
    setUpdateName(product.name);
    setUpdateDescription(product.description);
    setUpdateSku(product.sku);
    setUpdateQuantity(product.quantity);
    setUpdateImage(product.image);
    setUpdatePrice(product.price);
    setUpdateWidth(product.width);
  };
  
  const updateProduct = async () => {
    try {
      await axios.put(`${import.meta.env.VITE_API_URL}/api/product/${editingId}`, {
        name_update,
        description_update,
        sku_update,
        quantity_update,
        image_update,
        price_update,
        width_update,
      });

      const updatedProducts = products.map((product) =>
        product.id === editingId
          ? {
              ...product,
              name_update,
              description_update,
              sku_update,
              quantity_update,
              image_update,
              price_update,
              width_update,
            }
          : product
      );
      setProducts(updatedProducts);
      setEditingId(null);
      alert(`Product "${name_update}" updated successfully!`);
      fetchProducts();
    } catch (error) {
      console.error('Error updating product:', error);
    }
  };


  return (
    <div>
      <h2>Add Options to the Product</h2>
      <style>{`
        .product-table {
          width: 100%;
          border-collapse: collapse;
        }
        .product-table thead tr {
          background-color: #f8f8f8;
          color: #333;
          font-weight: bold;
        }
        .product-table td,
        .product-table th {
          padding: 8px;
          text-align: left;
          border: 1px solid #ddd;
        }
        .product-row:hover {
          background-color: #f1f1f1;
          cursor: pointer;
        }
        .product-table input {
          width: 100%;
          box-sizing: border-box;
        }
        .product-row:hover {
          background-color: #f1f1f1;
          cursor: pointer;
        }
        
      `}</style>
      <table className="product-table">
        <thead>
          <tr className="product-row">
            <th style={{width: "50px"}}>Product ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>SKU</th>
            <th>Manufacturer</th>
            <th style={{width: "50px"}}>Quantity</th>
            <th>Image</th>
            <th style={{width: "50px"}}>Price</th>
            <th style={{width: "50px"}}>Width</th>
            <th style={{width: "50px"}}>Options</th>
            <th>Date Added</th>
            <th style={{width: "200px"}}>Delete/Add Product</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
           
            <tr
              id={product.id}
              key={product.id}
              className="product-row"
              style={{
                backgroundColor: editingId === product.id ? '#fdd02e' : '',
                color: editingId === product.id ? '#391145' : '',
              }}>
              <td>{product.id}</td>
              <td>{product.name}</td>
              <td>{product.description}</td>
              <td>{product.sku}</td>
              <td>{product.manufacturer_name}</td>
              <td>{product.quantity}</td>
              <td>
                <img  width="200px" src={product.image} alt={product.name}/>
              </td>
              <td>{product.price}</td>
              <td>{product.width}</td>
              <td>{product.options.map((option) => (
                <div key={option.option_id}>
                  <img  width="100px" src={option.option_image} alt={option.option_name}/>
                </div>
              ))}</td>
              <td>{product.date_added}</td>
              <td>
                <button className="button-delete" onClick={() => deleteProduct(product.id)}>
                  Delete
                </button>
                <button className="button-update" onClick={() => startUpdate(product)}>Update</button>
              </td>
            </tr>
          ))}

          {editingId && (
          <tr style={{
            backgroundColor: '#6dd0fe',

          }} >
            <td>Update Product</td>
    <td>
      <input type="text" value={name_update} onChange={(e) => setUpdateName(e.target.value)} required />
    </td>
    <td>
      <input type="text" value={description_update} onChange={(e) => setUpdateDescription(e.target.value)} required />
    </td>
    <td>
      <input type="text" value={sku_update} onChange={(e) => setUpdateSku(e.target.value)} required />
    </td>
    <td>
      <input type="number" value={quantity_update} onChange={(e) => setUpdateQuantity(e.target.value)} required />
    </td>
    <td>
      <input type="text" value={image_update} onChange={(e) => setUpdateImage(e.target.value)} required />
    </td>
    <td>
      <input type="number" step="0.01" value={price_update} onChange={(e) => setUpdatePrice(e.target.value)} required />
    </td>
    <td>
      <input type="number" value={width_update} onChange={(e) => setUpdateWidth(e.target.value)} required />
    </td>
    <td></td>
    <td></td>
   
    
            <td>
              <button className="button-add" onClick={updateProduct}>Submit</button>
            </td>
          </tr>
        )}

<tr>
    <td>Create New Product</td>
    <td>
      <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
    </td>
    <td>
      <input type="text" value={description} onChange={(e) => setDescription(e.target.value)} required />
    </td>
    <td>
      <input type="text" value={sku} onChange={(e) => setSku(e.target.value)} required />
    </td>
  
    <td>
      <select 
        value={manufacturerId} onChange={(e) => setManufacturerId(e.target.value)} required>
        <option value="">--Please choose a manufacturer--</option>
        {manufacturers.map((manufacturer) => (
          <option key={manufacturer.id} value={manufacturer.id}>
            {manufacturer.name}
          </option>
        ))}
    </select>
    </td>
    <td>
      <input type="number" value={quantity} onChange={(e) => setQuantity(e.target.value)} required />
    </td>
    <td>
      <input type="text" value={image} onChange={(e) => setImage(e.target.value)} required />
    </td>
    <td>
      <input type="number" step="0.01" value={price} onChange={(e) => setPrice(e.target.value)} required />
    </td>
    <td>
      <input type="number" value={width} onChange={(e) => setWidth(e.target.value)} required />
    </td>
    <td>
   
   
    </td>
    <td></td>
    <td>
      <button className="button-add" type="submit" onClick={addProduct}>Add Product</button>
    </td>
  
  
</tr>

        </tbody>
      </table>
    </div>
  );
};

export default ProductList;
