import React from 'react';

export default class SaveModal extends React.Component {
  constructor(props) {
    super(props);
  }

  render(props) {
    return(
      <div className="modal" id="saveModal" tabIndex="-1" role="dialog" aria-labelledby="customModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
                <h3 id="customModalHeader">Cannot Save Block Selection</h3>
            </div>
            <div className="modal-body">
                <h4 id="customModalBody">
                  Invalid customization! Please make sure that the commands are matched to an unique color!
                </h4>
            </div>
            <div className="modal-footer">
                <button className="btn btn-primary pb-btn" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div>
    )
  }
}