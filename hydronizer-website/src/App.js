import './App.css';
import Navbar from "./components/Navbar/Navbar";
import InfoSection from "./components/InfoSection/InfoSection";
function App() {
  const device = "5843862085612977";

  return (
    <div className="App">
      <Navbar>
      
      </Navbar>
      <InfoSection device={device}>
        
      </InfoSection>
    </div>
  );
}

export default App;
