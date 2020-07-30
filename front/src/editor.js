    import React, { Component } from 'react';
    import {Link, withRouter} from 'react-router-dom';
    import {CopyToClipboard} from 'react-copy-to-clipboard';

    class Editor extends Component {
        // Stolen from https://dev.to/finallynero/using-websockets-in-react-4fkp
        // instance of websocket connection as a class property
        ws = new WebSocket('ws://localhost:5000/ws')
        lastEvent = ""
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
                this.lastEvent = 'connected'
            }
            
            this.ws.onmessage = evt => {
                // listen to data sent from the websocket server
                this.lastEvent = JSON.parse(evt.data)
                if (this.lastEvent.result === "fail") {
                    // Shit's fucked up yo, you did something you shouldn't
                    console.error("Status === fail")
                    console.error(this.lastEvent)
                } else if (this.lastEvent.result === "ok") {
                    console.log(this.lastEvent)
                    this.inputref.current.value = this.lastEvent.content
                } else {
                    console.error("Weird status")
                    console.error(this.lastEvent)
                }
            }
            
            this.ws.onclose = () => {
                this.last_event = 'disconnected'
            }
        }
        
        render() {
            return <div>
                <div>
                    <a href={window.location.href}>Link to this page</a> 
                    <CopyToClipboard text={window.location.href} onCopy={this.onLinkCopy}>
                        <button> Copy to clipboard </button>
                    </CopyToClipboard>
                    <Link to="/" color="red">Go home</Link>
                </div>
                <textarea id="textarea" rows="40" cols="150" ref={this.inputref} onChange={this.updateServer}></textarea>
            </div>;
        }
    }

    const EditorWithRouter = withRouter(Editor);
    export default EditorWithRouter;