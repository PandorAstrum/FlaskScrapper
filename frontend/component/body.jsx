import React from "react";

class Body extends React.Component {

  render() {
    return (
      
        <div class="grey lighten-3 position-absolute container-fluid text-dark">
        <h1 class="alpha-slab">Overview</h1>
        <div class="row">
            <div class="card medium white darken-1 col-lg-12"> 
                <div class="card-content black-text">
                    <span class="card-title">Job List</span>
                    <table> 
                        <thead> 
                            <tr> 
                                <th data-field="id">Job ID</th> 
                                <th data-field="name">Url</th> 
                                <th data-field="price">Status</th> 
                                <th data-field="name">Last Run</th> 
                                <th data-field="price">Run Time</th> 
                                <th data-field="price">Users</th> 
                            </tr>                         
                        </thead>                     
                        <tbody> 
                            <tr> 
                                <td># 1</td> 
                                <td>fb.com</td> 
                                <td>Success</td> 
                                <td>10 Days Ago</td> 
                                <td>35 Min</td> 
                                <td>500</td>
                            </tr>                         
                            <tr> 
                                <td># 1</td> 
                                <td>fb.com</td> 
                                <td>Success</td> 
                                <td>10 Days Ago</td> 
                                <td>35 Min</td> 
                                <td>500</td>
                            </tr>
                            <tr> 
                                <td># 1</td> 
                                <td>fb.com</td> 
                                <td>Success</td> 
                                <td>10 Days Ago</td> 
                                <td>35 Min</td> 
                                <td>500</td>
                            </tr>                         
                            <tr> 
                                <td># 1</td> 
                                <td>fb.com</td> 
                                <td>Success</td> 
                                <td>10 Days Ago</td> 
                                <td>35 Min</td> 
                                <td>500</td>
                            </tr>                         
                            <tr> 
                                <td># 1</td> 
                                <td>fb.com</td> 
                                <td>Success</td> 
                                <td>10 Days Ago</td> 
                                <td>35 Min</td> 
                                <td>500</td>
                            </tr>                         
                        </tbody>                     
                    </table>
                </div>             
                <div class="card-action flow-text">
                    <span>Showing 1 of 25 Pages</span>
                    <ul class="pagination right"> 
                        <li class="disabled">
                            <a href="#!"><i class="mdi-navigation-chevron-left"></i></a>
                        </li>                     
                        <li class="active">
                            <a href="#!">1</a>
                        </li>                     
                        <li class="waves-effect">
                            <a href="#!">2</a>
                        </li>                     
                        <li class="waves-effect">
                            <a href="#!">3</a>
                        </li>                     
                        <li class="waves-effect">
                            <a href="#!">4</a>
                        </li>                     
                        <li class="waves-effect">
                            <a href="#!">5</a>
                        </li>                     
                        <li class="waves-effect">
                            <a href="#!"><i class="mdi-navigation-chevron-right"></i></a>
                        </li>                     
                    </ul>                 
                </div>             
            </div>
        </div>
    </div>
    );
  }
}
export default Body;