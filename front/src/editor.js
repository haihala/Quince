import React, { Component } from 'react';
import {Link, withRouter} from 'react-router-dom';

class Editor extends Component {
    // Stolen from https://dev.to/finallynero/using-websockets-in-react-4fkp
    // instance of websocket connection as a class property
    ws = new WebSocket('ws://localhost:5000/ws')

    componentDidMount() {
        this.ws.onopen = () => {
        // on connecting, do nothing but log it to the console
        console.log('connected');
        this.ws.send("Mike");
        }

        this.ws.onmessage = evt => {
        // listen to data sent from the websocket server
        console.log(evt)
        }

        this.ws.onclose = () => {
        console.log('disconnected')
        }

    }
    
    render() {
        return <div>
            <p>
                {this.props.match.params.editorId}
            </p>
            <Link to="/" color="red"> Go home </Link>
            </div>;
    }
}

const EditorWithRouter = withRouter(Editor);
export default EditorWithRouter;