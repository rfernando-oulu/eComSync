import React, { useState, useEffect } from 'react';
import axios from 'axios';

const OrderList = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/order'); // Replace with your Flask API endpoint
      setOrders(response.data.orders);
    } catch (error) {
      console.error('Error fetching orders:', error);
    }
  };

  return (
    <div>
      <h2>Customer Orders</h2>
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
      `}</style>
      <table className="product-table">
        <thead>
          <tr className="product-row">
            <th>Customer Name</th>
            <th>Email</th>
            <th>Telephone</th>
            <th>Address</th>
            <th>City</th>
            <th>Postcode</th>
            <th>Country</th>
            <th>Total</th>
            <th>Date Added</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order, index) => (
            <tr key={index} className="product-row">
              <td>{order.firstname}</td>
              <td>{order.email}</td>
              <td>{order.telephone}</td>
              <td>{order.payment_address_1}</td>
              <td>{order.payment_city}</td>
              <td>{order.payment_postcode}</td>
              <td>{order.payment_country}</td>
              <td>${order.total}</td>
              <td>{order.date_added}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default OrderList;
