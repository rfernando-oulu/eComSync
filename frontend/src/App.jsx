import ProductList from './components/ProductList';
import OrderList from './components/OrderList';
import ManufacturerList from './components/ManufacturerList';
import OptionList from './components/OptionList';


function App() {
  return (
    <div className="App">
      <h1>eComSync 🛒- Integration of Amazon and eBay for eCommerce Online Retail Websites</h1>
      
      <ProductList />

      <OptionList />   

      <ManufacturerList />

      <OrderList />
      
    </div>
  )
}

export default App
