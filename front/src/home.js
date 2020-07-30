import React, { Component } from 'react';
import {Link} from 'react-router-dom';

class Home extends Component {
    render() {
        var d = new Date();
        var editor_url = "/editor/"+d.getTime();
        return <div>
            <p>Home</p>
            <Link to={editor_url} color="blue"> Go to editor </Link>
        </div>;
    }
}

export default Home;