/** @jsx React.DOM */
'use strict';
/**
* Video controls
*
*/

var CreateVideoView = React.createClass({displayName: 'CreateVideoView',
    handleDeleteVideo: function ( event ) {

        VideoResource.destroy( Video.slug ).defer().done(function ( data ) {
            window.location = Project.detail_url;
        });

    },
    handleChronicleClick: function ( event ) {
        window.location = Links.chronicle;
    },
    handlePublishClick: function ( event ) {
        window.location = Links.publish;
    },
    render: function () {
        var VideoUploader = VideoUploaderView({onMessage: this.props.onMessage, 
                                               uploader_config: UploaderConfig, 
                                               project: this.props.project})
        return (React.DOM.span(null, 
            React.DOM.span({onClick: this.handlePublishClick, className: "btn btn-primary btn-small pull-right"}, 
                React.DOM.i({className: "glyphicon glyphicon-eye-open"}), 
                React.DOM.span(null, "Publish")
            ), " ", 

            React.DOM.span({onClick: this.handleChronicleClick, className: "btn btn-primary btn-small pull-right"}, 
                React.DOM.i({className: "glyphicon glyphicon-road"}), 
                React.DOM.span(null, "Activity Chronicle")
            ), " ", 

            React.DOM.span({onClick: this.handleDeleteVideo, className: "btn btn-danger btn-small"}, 
                React.DOM.i({className: "glyphicon glyphicon-remove"}), 
                React.DOM.span(null, "Delete Video")
            ), " ", 
            VideoUploader
        ));
    }
});
