    import React, { Component } from 'react';
    import {Link, withRouter} from 'react-router-dom';
    import {CopyToClipboard} from 'react-copy-to-clipboard';

    class Editor extends Component {
        // Stolen from https://dev.to/finallynero/using-websockets-in-react-4fkp
        // instance of websocket connection as a class property
        ws = new WebSocket('ws://localhost:5000/ws')
        inputref = React.createRef();
        
        onLinkCopy() {
            // Maybe add visual flourish
        }
        
        updateServer() {
            // Send entire contents of the file to server
            this.ws.send(JSON.stringify({"type": "update", "id": this.props.match.params.editorId, "content": this.inputref.current.value}))
        }
        
        componentDidMount() {
            this.ws.onopen = () => {
                // on connecting, do nothing but log it to the console
                this.ws.send(JSON.stringify({"type": "fetch", "id": this.props.match.params.editorId}))
            }
            
            this.ws.onmessage = evt => {
                // listen to data sent from the websocket server
                let eventData = JSON.parse(evt.data)
                if (eventData.result === "fail") {
                    // Shit's fucked up yo, you did something you shouldn't
                    console.error("Status === fail")
                    console.error(eventData)
                } else if (eventData.result === "ok") {
                    console.log(eventData)
                    if (eventData.content) {
                        this.inputref.current.value = eventData.content
                    }
                } else {
                    console.error("Weird status")
                    console.error(eventData)
                }
            }
            
            this.ws.onclose = () => {
            }
        }
        
        render() {
            return <div>
                <div>
                    <a href={window.location.href}>Link to this page</a> 
                    <CopyToClipboard text={window.location.href} onCopy={this.onLinkCopy}>
                        <button>Copy to clipboard</button>
                    </CopyToClipboard>
                    <Link to="/" color="red">Go home</Link>
                </div>
                <textarea id="textarea" rows="40" cols="150" ref={this.inputref} onChange={this.updateServer.bind(this)}></textarea>
            </div>;
        }
    }

    const EditorWithRouter = withRouter(Editor);
    export default EditorWithRouter;