import React, { useState, useEffect } from 'react';
import { fetchManufacturersFunction } from './api';
import axios from 'axios';

const ManufacturerList = () => {
  const [manufacturers, setManufacturers] = useState([]);
  const [name, setName] = useState('');
  const [image, setImage] = useState('');
  const [description, setDescription] = useState('');

  const [editingId, setEditingId] = useState(null);

  const [name_update, setUpdateName] = useState('');
  const [description_update, setUpdateDescription] = useState('');
  const [image_update, setUpdateImage] = useState('');

  useEffect(() => {
    fetchManufacturers();
  }, []);

  const fetchManufacturers = async () => {
    try {
      
        setManufacturers(await fetchManufacturersFunction());

    } catch (error) {
        console.error('Error fetching manufacturers:', error);
    }
};

  const addManufacturer = async (e) => {
    e.preventDefault();

    try {
      await axios.post(`${import.meta.env.VITE_API_URL}/api/manufacturer/`, { // Replace with your Flask API endpoint
        name,
        image,
        description
      });

      setName('');
      setImage('');
      setDescription('');
      alert('Manufacturer added successfully!');
      fetchManufacturers();
    } catch (error) {
      console.error('Error adding manufacturer:', error);
    }
  };

  const deleteManufacturer = async (id) => {
    try {
      await axios.delete(`${import.meta.env.VITE_API_URL}/api/manufacturer/${id}`); // Replace with your Flask API endpoint
      alert('Manufacturer deleted successfully!');
      fetchManufacturers();
    } catch (error) {
      console.error('Error deleting manufacturer:', error);
    }
  };

  const startUpdate = (manufacturer) => {
    setEditingId(manufacturer.id);
    setUpdateName(manufacturer.name);
    setUpdateDescription(manufacturer.description);
    setUpdateImage(manufacturer.image);
  };

  const updateManufacturer = async () => {
    try {
      await axios.put(`http://127.0.0.1:5000/api/manufacturer/${editingId}`, {
        name_update,
        description_update,
        image_update,
      });

      const updatedManufacturers = manufacturers.map((manufacturer) =>
        manufacturer.id === editingId
          ? {
              ...manufacturer,
              name_update,
              description_update,
              image_update,
            }
          : manufacturer
      );
      setManufacturers(updatedManufacturers);
      setEditingId(null);
      alert(`Manufacturer "${name_update}" updated successfully!`);
      fetchManufacturers();
    } catch (error) {
      console.error('Error updating manufacturer:', error);
    }
  };


  return (
    <div>
      <h2>Manufacturers</h2>
      <style>{`
        .product-table {
          width: 100%;
          border-collapse: collapse;
          box-shadow: 10px 10px 10px #999;
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
            <th>Manufacturer ID</th>
            <th>Name</th>
            <th>Image</th>
            <th>Description</th>
            <th>Delete/Add Manufacturer</th>
          </tr>
        </thead>
        <tbody>
          {manufacturers.map((manufacturer) => (
            <tr id={manufacturer.id} 
                key={manufacturer.id} 
                className="product-row"
                style={{
                  backgroundColor: editingId === manufacturer.id ? '#fdd02e' : '',
                  color: editingId === manufacturer.id ? '#391145' : '',
                }}>
                
                <td>{manufacturer.id}</td>
              <td>{manufacturer.name}</td>
              <td><img width="150px" src={manufacturer.image} alt={manufacturer.name} /></td>
              <td>{manufacturer.description}</td>
              <td>
                <button className="button-delete" onClick={() => deleteManufacturer(manufacturer.id)}>
                  Delete
                </button>
                <button className="button-update" onClick={() => startUpdate(manufacturer)}>Update</button>
              </td>
            </tr>
          ))}

{editingId && (
          <tr style={{
            backgroundColor: '#6dd0fe',

          }} >
            <td>Update Manufacturer</td>
    <td>
      <input type="text" value={name_update} onChange={(e) => setUpdateName(e.target.value)} required />
    </td>
    <td>
      <input type="text" value={image_update} onChange={(e) => setUpdateImage(e.target.value)} required />
    </td>
    <td>
      <input type="text" value={description_update} onChange={(e) => setUpdateDescription(e.target.value)} required />
    </td>
    

            <td>
              <button className="button-add" onClick={updateManufacturer}>Submit</button>
            </td>
          </tr>
        )}

        <tr style={{ backgroundColor: '#f8f8f8'}}>
            <td>Create New Manufacturer</td>
            <td>
              <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" required />
            </td>
            <td>
              <input type="text" value={image} onChange={(e) => setImage(e.target.value)} placeholder="Image URL" required />
            </td>
            <td>
              <input type="text" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Description" required />
            </td>
            <td>
              <button className="button-add" onClick={addManufacturer}>Add Manufacturer</button>
            </td>
          </tr>

        </tbody>
      </table>
    </div>
  );
};

export default ManufacturerList;
