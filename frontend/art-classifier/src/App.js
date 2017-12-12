import React, { Component } from 'react';
import Dropzone from 'react-dropzone';
// eslint-disable-next-line
import request from 'superagent';
import logo from './art.png';
import loading from './loading.svg';
import ReactSvgPieChart from "react-svg-piechart";
import ToggleButton from 'react-toggle-button';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      file: '',
      imagePreviewUrl: '',
      stage: 'first',
      result: [],
      total: 0,
      highlighted: '',
      artist_toggle: true
    };
  }
  onImageDrop(files) {
      let file = files[0]
      this.setState({
        file: file,
        imagePreviewUrl: file.preview,
        stage: 'second'
      });
      this.handleImageUpload(file);
  }
  handleImageUpload(file) {
    const request_url = this.state.artist_toggle ? "/artist" : "/style";
    let upload = request.post(request_url)
                     .field('image', file);
    upload.end((err, response) => {
      if (err) {
        console.error(err);
      } else {
        this.setState({
          result: response.body["result"],
          total: parseFloat(response.body["total"]),
          highlighted: response.body["top"],
          stage: 'third',
        });
      }
    });
  }


  render() {
    let {imagePreviewUrl} = this.state;
    let {result} = this.state;
    let {stage} = this.state;
    let $imagePreview = null;
    let $resultList = null;
    let $pieChart = null;
    if (imagePreviewUrl) {
      // eslint-disable-next-line
      $imagePreview = (<img src={imagePreviewUrl} className="imageStored"/>);
    } else {
      $imagePreview = (<div className="previewText">Waiting for you to upload an image :) </div>);
    }
    if (stage === "third") {
      $resultList = (<div className="scoreContainer">
        <ul className="scoreList">{result.map((x, i) => {
          if (x['identifier'] === this.state.highlighted) {
            return (<li className="scoreItemHighlight" key={i}>
              <div className="identifierSubItem">{x['identifier']}</div>
              <div className="scoreSubItem">{x['score']}</div>
            </li>);
          } else {
            return (<li className="scoreItem" key={i}>
              <div className="identifierSubItem">{x['identifier']}</div>
              <div className="scoreSubItem">{x['score']}</div>
            </li>);
          }}
        )}</ul></div>);
        const data = [
          {title: result[0]["identifier"],
          value: parseFloat(result[0]["score"])/this.state.total, color: "#22594e"},
          {title: result[1]["identifier"],
          value: parseFloat(result[1]["score"])/this.state.total, color: "#2f7d6d"},
          {title: result[2]["identifier"],
          value: parseFloat(result[2]["score"])/this.state.total, color: "#3da18d"},
          {title: result[3]["identifier"],
          value: parseFloat(result[3]["score"])/this.state.total, color: "#69c2b0"},
          {title: result[4]["identifier"],
          value: parseFloat(result[4]["score"])/this.state.total, color: "#a1d9ce"}]
      $pieChart = (
        <ReactSvgPieChart
            data={data}
            expandOnHover={true}
            expandSize={5}
            shrinkOnTouchEnd={false}
            viewBoxSize={100}
            strokeWidth={1}
            stlye="{{cursor: pointer}}"
            onSectorHover={(d, i, e) => {
              if (d) {
                this.setState({'highlighted': d["title"]})
              }
            }}/>);

    } else if (stage === "second"){
      // eslint-disable-next-line
      $resultList = (<img src={loading} className="Loading" />);
      // eslint-disable-next-line
      $pieChart = (<img src={loading} className="Loading" />);
    } else {
      $pieChart = (<div className="previewText">Waiting for you to upload an image :) </div>);
      $resultList = (<div className="previewText">Waiting for you to upload an image :) </div>);
    }
    return (
      <div className="App">
        <header className="App-header">
          <div>
            <img src={logo} className="App-logo" alt="logo" />
            <h1 className="App-title">Welcome to Tagger</h1>
          </div>
          <div></div>
          <div>
            <h1 className="App-title">Painting Analysis</h1>
            <h1 className="App-title-2">Toggle Artist/Style</h1>
            <div className="toggleButton">
              <div></div>
              <div>
              <ToggleButton
                inactiveLabel={"Style"}
                activeLabel={"Artist"}
                value={this.state.artist_toggle}
                onToggle={(value) => {
                  this.setState({
                    artist_toggle: !value,
                  })
                }} />
              </div>
            </div>
          </div>
          <div></div>
          <div>
            <Dropzone
              className="dropImageBox"
              multiple={false}
              accept="image/*"
              onDrop={this.onImageDrop.bind(this)}>
              <p>Drag/Drop Image or Click to Upload</p>
            </Dropzone>
          </div>
        </header>
        <div className="previewComponent">
          <div className="imgPreview">
            {$imagePreview}
          </div>
          <div>
            {$resultList}
          </div>
          <div>
            {$pieChart}
          </div>
        </div>
      </div>
    );
  }
}

export default App;
