/** @jsx React.DOM */
/**
* Flowplayer
*
*/
// flowplayer
var FlowPlayerView = React.createClass({
    render: function () {
        var video_url = this.props.video.video_url;
        var video_type = this.props.video.video_type;
        var video_subtitles_url = this.props.video.video_subtitles_url;
        return (
            <div className="flowplayer">
               <video>
                <source src={video_url} type={video_type} />
                    <track src={video_subtitles_url} />
               </video>
            </div>
        );
    }
});