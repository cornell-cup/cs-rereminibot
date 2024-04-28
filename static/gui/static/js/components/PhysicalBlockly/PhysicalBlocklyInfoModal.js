import React from 'react';

export default class PhysicalBlocklyInfoModal extends React.Component {
    render(props) {
        return (
            <div className="modal fade" id="pbinfo" tabIndex="-1" role="dialog" aria-labelledby="pbInfoModalLabel" aria-hidden="true">
                <div className="modal-dialog" role="document">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title" id="pbInfoModalLabel">Physical Blockly Guide</h5>
                            <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div className="modal-body" id="pbInfoModal">
                            Make sure that you are connected to a bot before continuining.
                            You can use the toggle boxes in the customization section to select which color corresponds to which command.
                            Make sure to save your selections and then you can use start programming/live mode see the results!
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-secondary" data-dismiss="modal">I got this!</button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}