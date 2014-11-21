/** @jsx React.DOM */
'use strict';

var VideoUploaderView = React.createClass({
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

                    progress_bar.width(percent+'%');
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

                    ProjectVideoResource.create( video_object ).defer().done(function ( data ) {
                        // progress.addClass('hide');
                        // progress_bar.width('0%');

                        // progress_conversion.removeClass('hide');
                        // progress_conversion_bar.width('0%');
                        window.location = data.video_view_url;
                    });
                },
            });
        } // end validVideoFile
    },
    render: function () {
        return (<span>
            <span className="btn btn-success btn-small fileinput-button">
                <i className="glyphicon glyphicon-plus"></i>
                <span>New Video</span>
                <input id="fileupload" onChange={this.handleNewFile} ref="fileupload" type="file" name="video"/>
            </span>
            <br/>
            <br/>
            <div id="progress" className="progress hide">
                <div className="progress-bar progress-bar-success"></div>
            </div>
            <div id="progress-conversion" className="progress hide">
                <div className="progress-bar progress-bar-success"></div>
            </div>
            <div id="files" className="files"></div>
        </span>);
    }
});