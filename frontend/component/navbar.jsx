import React from 'react';
import mainlogo from '../static/assets/store_icon_black.png';
class Navbar extends React.Component {

    render() {
      return (
        <div className="navbar-fixed aclonica">
            <nav> 
                <div className="nav-wrapper white z-depth-1"> 
                    <a href="#" class="brand-logo black-text">
                        <img src={mainlogo} width="30" height="30" alt="" class="ml-5" />
                        Merchant
                    </a>                     
                    <ul id="nav-mobile" className="right hide-on-med-and-down"> 
                        <li>
                            <a className="btn waves-effect">Start a Job</a>
                        </li>                         
                        <li>
                            <a href="#" className="black-text waves-effect"><i className="mdi-social-notifications-none"></i></a>
                        </li>                         
                        <li> 
                            <a className="dropdown-button black-text waves-effect" href="#!" data-activates="dropdown1"> 
                                <img className="img-thumbnail circle rounded-circle" alt="" src="assets/img/Circle-icons-profle.svg.png" width="50" height="50" />
                                <i className="material-icons right">keyboard_arrow_down</i> 
                            </a>                             
                            <ul id="dropdown1" className="dropdown-content"> 
                                <li>
                                    <a href="#!">Edit Profile</a>
                                </li>                                 
                                <li>
                                    <a href="#!">Sign out</a>
                                </li>                                 
                                <li class="divider"></li>                                                                 
                            </ul>                             
                        </li>                         
                    </ul>                     
                </div>                 
            </nav>
        </div>
      );
    }
  }
  export default Navbar;