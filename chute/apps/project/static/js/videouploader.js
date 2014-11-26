/** @jsx React.DOM */
'use strict';

var VideoUploaderView = React.createClass({displayName: 'VideoUploaderView',
    getInitialState: function() {
        return {
            'uploader': new Evaporate(this.props.uploader_config),
            'states': ['base', 'preview', 'uploading', 'canceled', 'done'],
            'current_state': 'base',
        }
    },
    componentDidMount: function () {
        var self = this;
    },
    validVideoFile: function ( file ) {
        if ( file !== undefined ) {
            var types = file.type.split('/');
            if ( types[0] === 'video' ) {
                return true;
            }
        }
        return false;
    },
    handleNewFile: function ( event ) {
        event.preventDefault();

        this.props.onMessage( [] ); // reset

        var self = this;
        var config = this.props.uploader_config;
        var file = event.target.files[0];

        console.log(file);

        if ( this.validVideoFile( file ) !== true ) {

            this.props.onMessage([{
                'message': 'Could not upload {file_name} because its not a recognised video file. It appears to be {type} but needs to be video/mp4|mov|avi.'.assign({'file_name': file.name, 'type': file.type}),
                'type': 'warning'
            }]);

        } else { // validVideoFile

            var progress = $('div#progress');
            var progress_bar = progress.find('div.progress-bar');
            var progress_conversion = $('div#progress-conversion');
            var progress_conversion_bar = progress_conversion.find('div.progress-bar');

            progress.removeClass('hide');
            progress_bar.width('0%');

            progress_conversion.addClass('hide');
            progress_conversion_bar.width('0%');

            self.state.uploader.add({
                name: config.aws_path + file.name,
                file: file,
                xAmzHeadersAtInitiate: {
                    //'Cache-Control': 'max-age=86400',
                    'x-amz-acl': 'public-read',
                },
                progress: function ( progress_count ) {
                    console.log('progress:' + progress_count);
                    var percent = Math.round(progress_count * 100)
                    var percent_string = percent + '%';
                    progress_bar.width(percent_string);
                    self.props.onProgress( progress_count, percent_string );
                },
                complete: function ( data ) {
                    // post the new video event
                    var response = $(data.responseText);
                    var location = response.find('Location');
                    // video_url

                    var video_object = {
                        name: file.name,
                        video_url: location.text(),
                        video_type: file.type,
                    };

                    self.props.onUploadDone(data);
                },
            });
        } // end validVideoFile
    },
    render: function () {
        return (React.createElement("span", null, 
            React.createElement("span", {className: "btn btn-success btn-small fileinput-button"}, 
                React.createElement("i", {className: "glyphicon glyphicon-plus"}), 
                React.createElement("span", null, "New Video"), 
                React.createElement("input", {id: "fileupload", onChange: this.handleNewFile, ref: "fileupload", type: "file", name: "video"})
            ), 
            React.createElement("br", null), 
            React.createElement("br", null), 
            React.createElement("div", {id: "progress", className: "progress hide"}, 
                React.createElement("div", {className: "progress-bar progress-bar-success"})
            ), 
            React.createElement("div", {id: "progress-conversion", className: "progress hide"}, 
                React.createElement("div", {className: "progress-bar progress-bar-success"})
            ), 
            React.createElement("div", {id: "files", className: "files"})
        ));
    }
});