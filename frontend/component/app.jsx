import React from "react";
import Navbar from "./navbar";
import Body from "./body.jsx";
class App extends React.Component {

  render() {
    return (
      
      <div>
          <Navbar />
          <Body />
      </div>
    );
  }
}
export default App;