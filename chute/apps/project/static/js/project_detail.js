/** @jsx React.DOM */
'use strict';
/**
* Project detail controls
*
*/
var AddFeedItemBtn = React.createClass({displayName: 'AddFeedItemBtn',
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
        return (React.DOM.button({onClick: this.handleClick, className: "btn btn-success btn-xs"}, 
            React.DOM.span({className: "glyphicon glyphicon-plus"})
        ));
    }
});

var RemoveFeedItemBtn = React.createClass({displayName: 'RemoveFeedItemBtn',
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
        return (React.DOM.button({onClick: this.handleClick, className: "btn btn-xs"}, 
            React.DOM.span({className: "glyphicon glyphicon-remove"})
        ));
    }
});


// title view
var FeedNodeView = React.createClass({displayName: 'FeedNodeView',
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
            add_btn = AddFeedItemBtn({current_playlist: this.props.current_playlist, 
                                      node: node})
        }

        if ( is_in_playlist === true ) {
            remove_btn = RemoveFeedItemBtn({current_playlist: this.props.current_playlist, 
                                            node: node})

        }

        var pictureStyle = {
            'background-image': 'url('+ node.picture +')',
        };

        return (React.DOM.a({href: "javascript:;", 
                   onClick: this.handleClick.bind( this, node), 
                   onDragStart: this.handleDragStart, 
                   onDragOver: this.handleDragOver, 
                   onDrop: this.handleDrop, 
                   style: pictureStyle, 
                   className: "feeditem_list_picture list-group-item"}, 

                React.DOM.div({className: "col-xs-8"}, 
                    React.DOM.h4({className: "list-group-item-heading"}, node.name), 
                    React.DOM.p({className: "list-group-item-text"}, updated_at)
                ), 
                React.DOM.div({className: "col-xs-1"}, 
                    add_btn, 
                    remove_btn
                )
            ));
    }
});


// base view
var FeedView = React.createClass({displayName: 'FeedView',
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
            return FeedNodeView({current_playlist: self.state.current_playlist, 
                                 show_add_btn: show_add_btn, 
                                 is_in_playlist: is_in_playlist, 
                                 node: node});
        });

        return (React.DOM.span(null, 
          React.DOM.h3(null, "Complete Feed"), 
          React.DOM.nav({className: "navbar navbar-default", role: "navigation"}, 
            React.DOM.div({className: "container-fluid"}, 

                React.DOM.button({type: "button", className: "btn btn-success btn-sm"}, 
                  React.DOM.span({className: "glyphicon glyphicon glyphicon-plus"}), " Ad"
                ), 

                React.DOM.form({className: "form-inline pull-right", role: "form"}, 
                    React.DOM.div({className: "form-group"}, 
                      React.DOM.input({type: "text", className: "form-control input-sm col-xs-2", id: "q", placeholder: "Search..."})
                    )
                )

            )
          ), 
          React.DOM.div({className: "list-group"}, 
                feedNodes
          )
        ));

    },
});

var PlaylistView = React.createClass({displayName: 'PlaylistView',
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
            return FeedNodeView({current_playlist: self.state.current_playlist, 
                                 show_add_btn: show_add_btn, 
                                 is_in_playlist: is_in_playlist, 
                                 node: node});
        });

        var playlistNodes = this.state.playlists.map( function ( playlist ) {
            var css_class = (playlist.name === self.state.current_playlist.name) ? 'active' : '' ;
            return (React.DOM.li({className: css_class}, React.DOM.a({href: "#"}, playlist.name)));
        });

        return (React.DOM.span(null, 
          React.DOM.h3(null, "Playlist"), 
          React.DOM.nav({className: "navbar navbar-default", role: "navigation"}, 
            React.DOM.div({className: "container-fluid"}, 

                React.DOM.ul({className: "nav navbar-nav"}, 
                    React.DOM.li({className: "dropdown"}, 
                        React.DOM.a({href: "#", className: "dropdown-toggle", 'data-toggle': "dropdown"}, "Playlists ", React.DOM.span({className: "caret"})), 
                        React.DOM.ul({className: "dropdown-menu", role: "menu"}, 
                            React.DOM.li({className: "btn btn-success"}, React.DOM.a({href: "#"}, "Add Playlist")), 
                            React.DOM.li({className: "divider"}), 
                            playlistNodes
                        ), 
                        React.DOM.li(null, React.DOM.a({href: "#"}, this.state.current_playlist.name))
                    )
                )

            )
          ), 
          React.DOM.div({className: "draggable list-group"}, 
                feedNodes
          )
        ));

    },
});

// render the Base set
React.renderComponent(
  FeedView(null),
  document.getElementById('feed-list')
);

React.renderComponent(
  PlaylistView(null),
  document.getElementById('playlist-feed-list')
);

// render the collaborators
React.renderComponent(
  CollaboratorListView(null),
  document.getElementById('project-detail-collaborators')
);