import React from 'react';

export default class SelectionBox extends React.Component {
    constructor(props) {
        super(props);
    }

    render(props) {
        return (
            <div className="container selectionBox" style={{marginBottom: "10px"}}>
                 <div className="row">
                    <div className="col">
                        <label htmlFor="selection">{this.props.command}</label>
                    </div>
                    <div className="col">
                        <select className="custom-select custom-select-sm" id={this.props.command} onChange={(event) => 
                            this.props.changeSelection(event, this.props.pb, event.target.id, event.target.value)}>
                            {
                                this.props.choiceList.map((c) => c === this.props.default 
                                ? <option selected value={c} key={this.props.command + c}>{c}</option> 
                                : <option value={c} key={this.props.command + c}>{c}</option>)
                            }
                        </select>
                    </div>
                </div>
            </div>
        );
    }
}