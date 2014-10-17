/** @jsx React.DOM */
/**
* Flowplayer
*
*/
// flowplayer
var FlowPlayerView = React.createClass({displayName: 'FlowPlayerView',
    render: function () {
        var video_url = this.props.video.video_url;
        var video_type = this.props.video.video_type;
        var video_subtitles_url = this.props.video.video_subtitles_url;
        return (
            React.DOM.div({className: "flowplayer"}, 
               React.DOM.video(null, 
                React.DOM.source({src: video_url, type: video_type}), 
                    React.DOM.track({src: video_subtitles_url})
               )
            )
        );
    }
});