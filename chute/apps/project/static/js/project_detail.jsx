/** @jsx React.DOM */
'use strict';
/**
* Project detail controls
*
*/
// title view
var FeedNodeView = React.createClass({
    render: function () {
        var node = this.props.node;
        var updated_at = moment(node.updated_at).fromNow();

        console.log(node)
        return (<a href="#" className=" list-group-item">
                <img src={node.picture} alt={node.name} className="img-rounded col-xs-5 pull-right" />

                <h4 className="list-group-item-heading">{node.name}</h4>
                <p className="list-group-item-text">{updated_at}</p>
            </a>);
    }
});


// base view
var FeedView = React.createClass({
    getInitialState: function () {
        return {
            'feed': Project.feed
        }
    },
    onMessage: function ( messages ) {
        var self = this;
        this.setState({
            'messages': messages,
        });
        // reset messages after a time period
        // $.delay( 5200, function ( a ) {
        //     $('.messages').fadeOut( 'slow' );
        // });
    },
    render: function () {
        var feedNodes = this.state.feed.map( function( node ) {
            return <FeedNodeView node={node} />;
        });

        return (<span>
          <h3>Complete Feed</h3>
          <nav className="navbar navbar-default" role="navigation">
            <div className="container-fluid">

                <button type="button" className="btn btn-success btn-sm">
                  <span className="glyphicon glyphicon glyphicon-plus"></span> Ad
                </button>

                <form className="form-inline pull-right" role="form">
                    <div className="form-group">
                      <input type="text" className="form-control input-sm col-xs-2" id="q" placeholder="Search..." />
                    </div>
                </form>

            </div>
          </nav>
          <div className="list-group">
                {feedNodes}
          </div>
        </span>);

    },
});

var PlaylistView = React.createClass({
    getInitialState: function () {
        var current_playlist = Playlist[0] || {'feed': []};
        return {
            'playlists': Playlist,
            'current_playlist': current_playlist,
            'feed': current_playlist.feed
        }
    },
    onMessage: function ( messages ) {
        var self = this;
        this.setState({
            'messages': messages,
        });
    },
    render: function () {
        var self = this;

        var feedNodes = this.state.feed.map( function( node ) {
            return <FeedNodeView node={node} />;
        });

        var playlistNodes = this.state.playlists.map( function ( playlist ) {
            var css_class = (playlist.name === self.state.current_playlist.name) ? 'active' : '' ;
            return (<li className={css_class}><a href="#">{playlist.name}</a></li>);
        });

        return (<span>
          <h3>Playlist</h3>
          <nav className="navbar navbar-default" role="navigation">
            <div className="container-fluid">

                <ul className="nav navbar-nav">
                    <li className="dropdown">
                        <a href="#" className="dropdown-toggle" data-toggle="dropdown">Playlists <span className="caret"></span></a>
                        <ul className="dropdown-menu" role="menu">
                            <li className="btn btn-success"><a href="#">Add Playlist</a></li>
                            <li className="divider"></li>
                            {playlistNodes}
                        </ul>
                        <li><a href="#">{this.state.current_playlist.name}</a></li>
                    </li>
                </ul>

            </div>
          </nav>
          <div className="list-group">
                {feedNodes}
          </div>
        </span>);

    },
});

// render the Base set
React.renderComponent(
  <FeedView />,
  document.getElementById('feed-list')
);

React.renderComponent(
  <PlaylistView />,
  document.getElementById('playlist-feed-list')
);

// render the collaborators
React.renderComponent(
  <CollaboratorListView />,
  document.getElementById('project-detail-collaborators')
);