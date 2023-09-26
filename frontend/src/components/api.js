import axios from 'axios';

export const fetchManufacturersFunction = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/manufacturer/`, {
      headers: { 'access-key': import.meta.env.VITE_ACCESS_KEY }
    });

    const manufacturersWithDetails = await Promise.all(
      response.data.items.map(async item => {
        const manufacturerDetailResponse = await axios.get(`${import.meta.env.VITE_API_URL}${item["@controls"]["storage:manufacturer"]["href"]}`);
        return manufacturerDetailResponse.data.manufacturer[0];
      })
    );

    return manufacturersWithDetails;
  } catch (error) {
    console.error('Error fetching manufacturers:', error);
    return [];  // return an empty array on error
  }
};
