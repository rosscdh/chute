/** @jsx React.DOM */
'use strict';
/**
* Project detail controls
*
*/
var AddFeedItemBtn = React.createClass({
    handleClick: function ( e ) {
        var node = this.props.node;
        var playlist = this.props.current_playlist;
        var form_data = {
                'feeditem': node.pk
            },
            route_params = {
                'pk': playlist.pk,
            };

        ProjectPlaylistFeedResource.create( form_data, route_params ).defer().done(function ( data ) {

            console.log(data);

        });
    },
    render: function () {
        return (<button onClick={this.handleClick} className="btn btn-success btn-xs">
            <span className="glyphicon glyphicon-plus"></span>
        </button>);
    }
});

var RemoveFeedItemBtn = React.createClass({
    handleClick: function ( e ) {
        var node = this.props.node;
        var playlist = this.props.current_playlist;
        var route_params = {
                'pk': playlist.pk,
            };

        ProjectPlaylistFeedResource.destroy( node.pk, route_params ).defer().done(function ( data ) {

            console.log(data);

        });
    },
    render: function () {
        return (<button onClick={this.handleClick} className="btn btn-xs">
            <span className="glyphicon glyphicon-remove"></span>
        </button>);
    }
});


// title view
var FeedNodeView = React.createClass({
    handleClick: function ( node, event ) {
        //event.preventDefault();
        var iframe = $('iframe#feed-item-detail');
        iframe.attr('src', node.absolute_url)
        iframe.height(iframe.contents().height());
    },
    handleDragStart: function ( e ) {
        console.log(e);
    },
    handleDragOver: function ( e ) {
        console.log(e);
    },
    handleDrop: function ( e ) {
        console.log(e);
    },
    render: function () {
        var node = this.props.node;
        var updated_at = moment(node.updated_at).fromNow();
        var is_in_playlist = this.props.is_in_playlist || false;
        var show_button = this.props.show_add_btn || false;
        var add_btn = null;
        var remove_btn = null;

        if ( is_in_playlist === false && show_button === true ) {
            add_btn = <AddFeedItemBtn current_playlist={this.props.current_playlist}
                                      node={node} />
        }

        if ( is_in_playlist === true ) {
            remove_btn = <RemoveFeedItemBtn current_playlist={this.props.current_playlist}
                                            node={node} />

        }

        var pictureStyle = {
            'background-image': 'url('+ node.picture +')',
        };

        return (<a href="javascript:;"
                   onClick={this.handleClick.bind( this, node )}
                   onDragStart={this.handleDragStart}
                   onDragOver={this.handleDragOver}
                   onDrop={this.handleDrop}
                   style={pictureStyle}
                   className="feeditem_list_picture list-group-item">

                <div className="col-xs-8">
                    <h4 className="list-group-item-heading">{node.name}</h4>
                    <p className="list-group-item-text">{updated_at}</p>
                </div>
                <div className="col-xs-1">
                    {add_btn}
                    {remove_btn}
                </div>
            </a>);
    }
});


// base view
var FeedView = React.createClass({
    getInitialState: function () {
        var current_playlist = Playlist[0] || {'feed': []};
        return {
            'playlists': Playlist,
            'current_playlist': current_playlist,
            'current_playlist_pks': this.playlistFeedItemPks( current_playlist ),
            'feed': Project.feed
        }
    },
    playlistFeedItemPks: function ( playlist ) {
        return playlist.feed.map( function( node ) {
            return node.pk
        });
    },
    feedIsInPlaylist: function ( feed_item ) {
        return this.state.current_playlist_pks.indexOf( feed_item.pk ) >= 0;
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
        var self = this;

        var feedNodes = this.state.feed.map( function( node ) {
            var show_add_btn = true;
            var is_in_playlist = self.feedIsInPlaylist( node );
            return <FeedNodeView current_playlist={self.state.current_playlist}
                                 show_add_btn={show_add_btn}
                                 is_in_playlist={is_in_playlist}
                                 node={node} />;
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

        var feedNodes = this.state.feed.map( function ( node ) {
            var show_add_btn = false;
            var is_in_playlist = true;
            return <FeedNodeView current_playlist={self.state.current_playlist}
                                 show_add_btn={show_add_btn}
                                 is_in_playlist={is_in_playlist}
                                 node={node} />;
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
          <div className="draggable list-group">
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