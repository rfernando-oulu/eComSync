import React, { useState, useEffect } from 'react';
import axios from 'axios';

const OptionList = () => {
  const [options, setOptions] = useState([]);
  const [name, setName] = useState('');
  const [image, setImage] = useState('');

  const [editingId, setEditingId] = useState(null);

  const [name_update, setUpdateName] = useState('');
  const [image_update, setUpdateImage] = useState('');

  useEffect(() => {
    fetchOptions();
  }, []);

  const fetchOptions = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/option/`, { 
        headers: { 'access-key': import.meta.env.VITE_ACCESS_KEY }
      });
      setOptions(response.data.options);
    } catch (error) {
      console.error('Error fetching options:', error);
    }
  };

  const addOption = async (e) => {
    e.preventDefault();

    try {
      await axios.post(`${import.meta.env.VITE_API_URL}/api/option/`, { // Replace with your Flask API endpoint
        name,
        image
      }, { 
        headers: { 'access-key': import.meta.env.VITE_ACCESS_KEY }
      });

      setName('');
      setImage('');
      alert('Option added successfully!');
      fetchOptions(); // Assuming you have a function called fetchOptions() that updates your state
    } catch (error) {
      console.error('Error adding option:', error);
    }
  };

  const deleteOption = async (id) => {
      try {
          await axios.delete(`${import.meta.env.VITE_API_URL}/api/option/${id}`, { 
              headers: { 'access-key': import.meta.env.VITE_ACCESS_KEY }
          });
          alert('Option deleted successfully!');
          fetchOptions();
      } catch (error) {
          console.error('Error deleting option:', error);
      }
  };

  const startUpdate = (option) => {
    setEditingId(option.id);
    setUpdateName(option.name);
    setUpdateImage(option.image);
  };

  const updateOption = async () => {
    try {
      await axios.put(`${import.meta.env.VITE_API_URL}/api/option/${editingId}`, {
        name_update,
        image_update,
      }, {
        headers: { 'access-key': import.meta.env.VITE_ACCESS_KEY }
      });
  
      const updatedOptions = options.map((option) =>
        option.id === editingId
          ? {
              ...option,
              name_update,
              image_update,
            }
          : option
      );
      setOptions(updatedOptions);
      setEditingId(null);
      alert(`Option "${editingId}" updated successfully!`);
      fetchOptions();
    } catch (error) {
      console.error('Error updating option:', error);
    }
  };
  

  return (
    <div>
      <h2>Product Options</h2>
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
            <th>Id</th>
            <th>Name</th>
            <th>Image</th>
            <th>Delete/Add Options</th>
          </tr>
        </thead>
        <tbody>
          {options.map((option, index) => (
              <tr id={option.id} 
                key={option.id} 
                className="product-row"
                style={{
                  backgroundColor: editingId === option.id ? '#fdd02e' : '',
                  color: editingId === option.id ? '#391145' : '',
                }}>
              <td>{option.id}</td>
              <td>{option.name}</td>
              <td><img width="150px" src={option.image} alt={option.name} /></td>
              <td>
                <button className="button-delete" onClick={() => deleteOption(option.id)}>
                  Delete
                </button>
                <button className="button-update" onClick={() => startUpdate(option)}>Update</button>
              </td>
            </tr>
          ))}

{editingId && (
          <tr style={{
            backgroundColor: '#6dd0fe',

          }} >
            <td>Update Option</td>
    <td>
      <input type="text" value={name_update} onChange={(e) => setUpdateName(e.target.value)} required />
    </td>
    <td>
      <input type="text" value={image_update} onChange={(e) => setUpdateImage(e.target.value)} required />
    </td>
    

            <td>
              <button className="button-add" onClick={updateOption}>Submit</button>
            </td>
          </tr>
        )}

          <tr style={{ backgroundColor: '#f8f8f8'}}>
            <td>Create New Product Option</td>
    
            <td>
              <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" required />
            </td>
            <td>
              <input type="text" value={image} onChange={(e) => setImage(e.target.value)} placeholder="image URL" required />
            </td>
            <td>
              <button className="button-add" onClick={addOption}>Add Product Option</button>
            </td>
          </tr>

        </tbody>
      </table>
    </div>
  );
};

export default OptionList;
