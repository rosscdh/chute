/** @jsx React.DOM */
/**
* Project chronicle controls
*
*/
var SearchForm = React.createClass({
    render: function () {
        return (<div className="row col-md-12">
            <form class="form-horizontal" role="form">
                <div className="form-group">
                    <div className="input-group search-field">
                        <input type="text" className="form-control input-lg" placeholder="Search comments by type, text or commenter..." name="q" autocomplete="off" onChange={this.props.onSearch}/>
                    </div>
                </div>
            </form>
        </div>);
    }
});


var ChronicleCommentsBase = React.createClass({
    fuse: new Fuse(Comments, { keys: ["comment_type", "comment_by", "comment", "progress"], threshold: 0.35 }),
    getInitialState: function () {
        return {
            'comments': Comments,
            'num_comments': Comments.length,
            'searched': true,
            'video': Video,
            'progress': 0,
            'flowplayer': null,
        }
    },
    onVideoUpdate: function ( video ) {
        this.setState({
            'video': video
        });
    },
    onSeekTo: function () {
        this.state.flowplayer.seek( seek_to );
    },
    onSearch: function ( event ) {
        var searchFor = event.target.value;
        var comments_results = (searchFor != '') ? this.fuse.search(event.target.value) : Comments;
        var searched = (searchFor != '') ? true : false;

        this.setState({
            'comments': comments_results,
            'num_comments': comments_results.length,
            'searched': searched,
        });
    },
    componentDidMount: function () {
        var self = this;
        /**
        * Flowplayer setup and configuration
        **/
        flowplayer(function ( api, root ) {
            //
            // Capture Events
            //
            api.conf.debug = false;
            api.conf.engine = 'html5';
            api.conf.preload = 'auto';
            api.conf.keyboard = false;

            api.bind("progress", function ( event, ob, progress ) {
                self.state.video.timestamp = progress;
                self.setState({
                    'progress': progress
                });
            });
            // set the state handler
            self.setState({
                'flowplayer': api
            });

        });
    },
    render: function () {
        var searchForm = <SearchForm onSearch={this.onSearch} />
        var flowPlayer = <FlowPlayerView video={this.state.video} />
        var show_comment_form = false;
        var commentsDetail = <CommentListView comments={this.state.comments}
                                              show_form={show_comment_form}
                                              onVideoUpdate={this.onVideoUpdate}
                                              onSeekTo={this.onSeekTo} />
        return (<div className="row">
            <div className="col-md-7">
                {flowPlayer}
            </div>
            <div className="col-md-5">
                {searchForm}
                {commentsDetail}
            </div>
        </div>);
    }
});
// render chronicle
React.renderComponent(
  <ChronicleCommentsBase />,
  document.getElementById('project-detail-chronicle')
);