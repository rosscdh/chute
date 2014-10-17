/** @jsx React.DOM */
/**
* Project collaborators
*
*/
// time indicator view - used as a display element in a number of other views
var TimestampView = React.createClass({
    secondsToStamp: function ( secs ) {
        var minutes = Math.floor(secs / 60);
        var seconds = (secs - minutes * 60).round(2);
        var hours = Math.floor(secs / 3600);
        //time = time - hours * 3600;
        return '{hours}:{minutes}:{seconds}'.assign({ 'seconds': seconds.pad(2), 'minutes': minutes.pad(2), 'hours': hours.pad(2) })
    },
    render: function () {
        var is_link = this.props.is_link || true;
        var progress_seconds = this.props.progress;
        var stamp = this.secondsToStamp( progress_seconds );
        var timestamp_link = '#' + stamp;
        var classNames = 'badge';

        var handleSeek = (this.props.onSeekTo !== undefined) ? this.props.onSeekTo.bind( this, progress_seconds ) : null ;

        if ( handleSeek !== null ) {
            return (<span className={classNames}>
            {handleSeek}
                <a href={timestamp_link} onClick={handleSeek}>{stamp}</a>
                </span>);
        } else {
            return (<span className={classNames}>
                {stamp}
                </span>);
        }
    }
});