import React from 'react';
import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import Home from './home';
import EditorWithRouter from './editor';

export default function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route path="/editor/:editorId">
            <EditorWithRouter />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

