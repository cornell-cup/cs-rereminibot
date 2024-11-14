import React from 'react';

export default class CustomBlockModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {selectedCustomBlock: []};
    this.initSelection = this.initSelection.bind(this);
    this.changeCustomBlockSelection = this.changeCustomBlockSelection.bind(this);
    this.handleSaveSelection = this.handleSaveSelection.bind(this);
    this.getLoopElements = this.getLoopElements.bind(this);
  }

  initSelection() {
    let selected = [];
    if (this.props.customBlocks.length == 0) return selected;
    for(var i = 0; i < this.props.customCount; i ++) {
      selected.push(null);
    }
    return selected;
  }

  changeCustomBlockSelection(e, id, value) {
    e.preventDefault();
    let selection = [];

    if(this.state.selectedCustomBlock == null || this.state.selectedCustomBlock.length == 0) {
      selection = this.initSelection();
    } else {
      selection = this.state.selectedCustomBlock;
    }

    selection[id] = value;
    this.setState({ selectedCustomBlock : selection});
  }

  getSelectList() {
    let selectList = [];
    let selectOption = [];
     
    // Create an empty option for the first option
    selectOption.push(<option key={0}>None</option>);

    for(var i = 1; i < this.props.customBlocks.length+1; i ++){
      selectOption.push(<option key={i}>{this.props.customBlocks[i-1][0]}</option>);
    }

    for(var i = 0; i < this.props.customCount; i ++) {
      let selectDropdown = <select key={i} id={i} defaultValue={"None"}
        onChange={(event) => this.changeCustomBlockSelection(event, event.target.id, event.target.value)}>
        {selectOption}
      </select>;
      selectList.push(<li key={i}>{selectDropdown}</li>);
    }
    
    return selectList;
  }

  getLoopElements() {
    let loopElements = [];
    for(var i = 0; i < this.props.loopCount; i ++) {
      let inputID = "n" + i;
      let label = <label>n{i}</label>;
      let input = <input className="loopNumberInput" type="number" placeholder={this.props.defaultLoopIteration} id={inputID} />;
      loopElements.push(<div className="loopSelector" key={i}>{label}{input}</div>);
    }

    return loopElements;
  }

  handleSaveSelection(e) {
    let loopSelection = [];
    for(var i = 0; i < this.props.loopCount; i ++) {
      let inputID = "n" + i;
      let value = document.getElementById(inputID).value;
      if (value == null || isNaN(parseInt(value)) || parseInt(value) < 1) {
        loopSelection.push(this.props.defaultLoopIteration);
      } else {
        loopSelection.push(parseInt(value));
      }
    }

    if (this.props.customBlocks.length <= 0) {
      this.props.saveSelection(e, loopSelection, []);
    }
    else if (this.state.selectedCustomBlock == null || this.state.selectedCustomBlock.length == 0) {
      let defaultCustomSelection = this.initSelection();
      this.props.saveSelection(e, loopSelection, defaultCustomSelection);
    } else {
      this.props.saveSelection(e, loopSelection, this.state.selectedCustomBlock);
    }
    this.setState({ selectedCustomBlock: [] });
  }

  render(props) {
    return(
      <div className="modal" id="customModal" tabIndex="-1" role="dialog" aria-labelledby="customModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
                <h3 id="customModalHeader">Physical Blockly Custom Selections</h3>
            </div>
            <div className="modal-body">
              <div className="container">
                <div className="row">   
                  {this.props.loopCount > 0 ? 
                    <div className="col">
                      <div id="loopIterationSection">
                        <h4 id="loopModalBody">
                          Enter number of iterations for each loop.
                        </h4>
                        <ol>
                          {this.getLoopElements()}
                        </ol>
                      </div>
                    </div> : <span></span>}
                  {this.props.customCount > 0 && this.props.customBlocks.length > 0 ?
                    <div className="col">
                      <div id="customBlockSection">
                        <h4 id="customModalBody">
                          Select a custom block function for each placeholder.
                        </h4>
                        <ol>
                          {this.getSelectList()}
                        </ol>
                      </div>
                    </div> : <div></div>}
                </div>
                {this.props.customCount > 0 && this.props.customBlocks.length > 0 ? 
                  <div className="row">
                    <h4 className="modalText" id="savedBlockTitle">Saved Custom Blocks</h4>
                    <div className="container">
                      {this.props.customBlocks.map((c, i) => <div className="customBlockObject" key={i}>
                        <button className="btn btn-primary customCollapseButton" type="button" data-toggle="collapse" data-target={"#" + "customCollapse" + i} aria-expanded="false" aria-controls={"customCollapse" + i}>
                          {c[0]}
                        </button>
                        <div className="collapse" id={"customCollapse" + i}>
                          <div className="card card-body customBlockContent">
                            <code>{c[1]}</code>
                          </div>
                        </div>
                      </div>)}
                    </div>
                  </div> : <span></span>}
              </div>
            </div>
            <div className="modal-footer">
                <button className="btn btn-primary pb-btn" onClick={(event) => this.handleSaveSelection(event)}>Save</button>
            </div>
          </div>
        </div>
      </div>
    )
  }
}