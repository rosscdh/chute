/** @jsx React.DOM */
'use strict';
/**
* Project detail controls
*
*/
// title view
var FeedNodeView = React.createClass({displayName: 'FeedNodeView',
    render: function () {
        var node = this.props.node;
        var updated_at = moment(node.updated_at).fromNow();

        console.log(node)
        return (React.DOM.a({href: "#", className: " list-group-item"}, 
                React.DOM.img({src: node.picture, alt: node.name, className: "img-rounded col-xs-5 pull-right"}), 

                React.DOM.h4({className: "list-group-item-heading"}, node.name), 
                React.DOM.p({className: "list-group-item-text"}, updated_at)
            ));
    }
});


// base view
var FeedView = React.createClass({displayName: 'FeedView',
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
            return FeedNodeView({node: node});
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

        var feedNodes = this.state.feed.map( function( node ) {
            return FeedNodeView({node: node});
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
          React.DOM.div({className: "list-group"}, 
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