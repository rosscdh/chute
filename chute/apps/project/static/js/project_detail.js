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
        return (React.createElement("button", {onClick: this.handleClick, className: "btn btn-success btn-xs"}, 
            React.createElement("span", {className: "glyphicon glyphicon-plus"})
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
        return (React.createElement("button", {onClick: this.handleClick, className: "btn btn-xs"}, 
            React.createElement("span", {className: "glyphicon glyphicon-remove"})
        ));
    }
});

var FeedPreviewView = React.createClass({displayName: 'FeedPreviewView',
    getInitialState: function () {
        return {
            'feed_item': Project.feed[0],
        }
    },
    handleFeedItemUpdate: function () {
        var self = this;
        var feed_item = self.state.feed_item;

        var params = {
            'wait_for': this.refs.wait_for.getDOMNode().value.trim(),
        };

        if ( window.feed_item_timer_event !== null ) {
            window.clearTimeout(window.feed_item_timer_event);
        }
        window.feed_item_timer_event = window.setTimeout(function() {

            FeedItemResource.update( feed_item.pk, params ).defer().done(function ( updated_feed_item ) {

                self.setState({
                    'feed_item': updated_feed_item
                });

                // send update signal
                $( 'body' ).trigger( 'update_feed_item', updated_feed_item );

            });

        }, 200);

    },
    handleFeedChange: function ( feed_item ) {
        this.setState({
            'feed_item': feed_item
        });

    },
    componentWillMount: function () {
        var self = this;
        $( 'body' ).on( 'select_feed', function ( event, feed_item ) {
            self.handleFeedChange( feed_item );
        });
    },
    componentDidMount: function () {
        var self = this;
        var iframe = $(this.refs.feed_item_detail.getDOMNode());

        iframe.on( 'load', function ( event ) {
            iframe.height(iframe.contents().height());
        });
    },
    render: function () {
        var feed_item = this.state.feed_item;

        var iframe_style = {
            'border': '0px;',
            'padding': '0px;',
            'width': '100%;',
            'height': '640px;',
        };

        return (React.createElement("span", null, 
          React.createElement("h3", null, "Preview"), 
          React.createElement("nav", {className: "navbar navbar-default", role: "navigation"}, 
            React.createElement("div", {className: "container-fluid"}, 
              React.createElement("div", {className: "row"}, 
                React.createElement("form", {className: "form-inline", role: "form"}, 
                    "#", feed_item.pk, 
                    React.createElement("div", {className: "form-group"}, 
                      React.createElement("div", {className: "input-group col-xs-9"}, 
                        React.createElement("div", {className: "input-group-addon"}, "show for"), 
                        React.createElement("input", {className: "form-control input-sm", ref: "wait_for", type: "integer", onChange: this.handleFeedItemUpdate, placeholder: "Number of", value: feed_item.wait_for}), 
                        React.createElement("div", {className: "input-group-addon"}, "sec")
                      )
                    ), 

                    React.createElement("div", {className: "form-group"}, 
                        React.createElement("ul", {className: "nav navbar-nav"}, 
                          React.createElement("li", {className: "dropdown"}, 
                            React.createElement("a", {href: "#", className: "dropdown-toggle", 'data-toggle': "dropdown"}, "Using Template ", React.createElement("span", {className: "caret"})), 
                            React.createElement("ul", {className: "dropdown-menu", role: "menu"}, 
                              React.createElement("li", null, 
                                React.createElement("a", {href: "#", className: "thumbnail"}, React.createElement("img", {'data-src': "holder.js/100%x100", alt: "..."}))
                              ), 
                              React.createElement("li", null, 
                                React.createElement("a", {href: "#", className: "thumbnail"}, React.createElement("img", {'data-src': "holder.js/100%x100", alt: "..."}))
                              ), 
                              React.createElement("li", null, 
                                React.createElement("a", {href: "#", className: "thumbnail"}, React.createElement("img", {'data-src': "holder.js/100%x100", alt: "..."}))
                              )
                            )
                          )
                        )
                    )
                )
              )
            )
          ), 
          React.createElement("iframe", {ref: "feed_item_detail", src: feed_item.absolute_url, border: "0", style: iframe_style})
        ));

    },
});

// title view
var FeedNodeView = React.createClass({displayName: 'FeedNodeView',
    getInitialState: function () {
        return {
            'node': this.props.node
        }
    },
    componentWillMount: function () {
        var self = this;
        $( 'body' ).on( 'update_feed_item', function ( e, updated_feed_item ) {
            if ( updated_feed_item.pk == self.props.node.pk ) {
                self.setState({
                    'node': updated_feed_item,
                });
            }
        });
    },
    handleClick: function ( node, event ) {
        event.preventDefault();
        $( 'body' ).trigger( 'select_feed', node );
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
        var node = this.state.node;
        var updated_at = moment(node.updated_at).fromNow();
        var is_in_playlist = this.props.is_in_playlist || false;
        var show_button = this.props.show_add_btn || false;
        var add_btn = null;
        var remove_btn = null;

        if ( is_in_playlist === false && show_button === true ) {
            add_btn = React.createElement(AddFeedItemBtn, {current_playlist: this.props.current_playlist, 
                                      node: node})
        }

        if ( is_in_playlist === true ) {
            remove_btn = React.createElement(RemoveFeedItemBtn, {current_playlist: this.props.current_playlist, 
                                            node: node})

        }

        var pictureStyle = {
            'background-image': 'url('+ node.picture +')',
        };

        return (React.createElement("a", {href: "javascript:;", 
                   onClick: this.handleClick.bind( this, node), 
                   onDragStart: this.handleDragStart, 
                   onDragOver: this.handleDragOver, 
                   onDrop: this.handleDrop, 
                   style: pictureStyle, 
                   className: "feeditem_list_picture list-group-item"}, 

                React.createElement("div", {className: "col-xs-8"}, 
                    React.createElement("h4", {className: "list-group-item-heading"}, node.name), 
                    React.createElement("p", {className: "small list-group-item-text"}, node.template_name, " (", node.post_type, ")"), 
                    React.createElement("p", {className: "small list-group-item-text"}, updated_at)
                ), 
                React.createElement("div", {className: "col-xs-1"}, 
                    add_btn, 
                    remove_btn
                )
            ));
    }
});


// base view
// var FeedView = React.createClass({
//     getInitialState: function () {
//         var current_playlist = Playlist[0] || {'feed': []};

//         return {
//             'playlists': Playlist,
//             'current_playlist': current_playlist,
//             'current_playlist_pks': this.playlistFeedItemPks( current_playlist ),
//             'feed': Project.feed,
//             'total_num_projects': Project.feed.length,
//             'searched': false,
//         }
//     },
//     playlistFeedItemPks: function ( playlist ) {
//         return playlist.feed.map( function( node ) {
//             return node.pk
//         });
//     },
//     feedIsInPlaylist: function ( feed_item ) {
//         return this.state.current_playlist_pks.indexOf( feed_item.pk ) >= 0;
//     },
//     onMessage: function ( messages ) {
//         var self = this;
//         this.setState({
//             'messages': messages,
//         });
//         // reset messages after a time period
//         // $.delay( 5200, function ( a ) {
//         //     $('.messages').fadeOut( 'slow' );
//         // });
//     },
//     render: function () {
//         var self = this;

//         var feedNodes = this.state.feed.map( function( node ) {
//             var show_add_btn = true;
//             var is_in_playlist = self.feedIsInPlaylist( node );
//             var key = 'feedlist-n-{pk}'.assign({'pk': node.pk});
//             return <FeedNodeView key={key}
//                                  current_playlist={self.state.current_playlist}
//                                  show_add_btn={show_add_btn}
//                                  is_in_playlist={is_in_playlist}
//                                  node={node} />;
//         });

//         return (<span>
//           <h3>Complete Feed</h3>
//           <nav className="navbar navbar-default" role="navigation">
//             <div className="container-fluid">

//                 <button type="button" className="btn btn-success btn-sm">
//                   <span className="glyphicon glyphicon glyphicon-plus"></span> Ad
//                 </button>

//                 <form className="form-inline pull-right" role="form">
//                     <div className="form-group">
//                       <input type="text" className="form-control input-sm col-xs-2" id="q" placeholder="Search..." />
//                     </div>
//                 </form>

//             </div>
//           </nav>
//           <div className="list-group">
//                 {feedNodes}
//           </div>
//         </span>);

//     },
// });

var PlaylistView = React.createClass({displayName: 'PlaylistView',
    getInitialState: function () {
        var current_playlist = Playlist[0] || {'feed': []};
        return {
            'playlists': Playlist,
            'current_playlist': current_playlist,
            'feed': current_playlist.feed,
            'total_num_items': current_playlist.feed.length,
        }
    },
    componentDidMount: function () {
        this.fuse = new Fuse(this.state.feed, {
            'keys': ['name', 'post_type'],
            'threshold': 0.35,
        });
    },
    handleSearch: function( event ) {
        var searchFor = event.target.value.trim();
        var search_results = (searchFor != '') ? this.fuse.search( searchFor ) : this.fuse.list;

        this.setState({
            'feed': search_results,
            'total_num_items': search_results.length,
        });
    },
    handleAddVideo: function ( event ) {
        window.location = Links.add_video;
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
            var key = 'playlist-node-{pk}'.assign({'pk': node.pk});
            return React.createElement(FeedNodeView, {key: key, 
                                 current_playlist: self.state.current_playlist, 
                                 show_add_btn: show_add_btn, 
                                 is_in_playlist: is_in_playlist, 
                                 node: node});
        });

        var playlistNodes = this.state.playlists.map( function ( playlist ) {
            var css_class = (playlist.name === self.state.current_playlist.name) ? 'active' : '' ;
            var key = 'playlist-{pk}'.assign({'pk': playlist.pk});
            return (React.createElement("li", {key: key, className: css_class}, React.createElement("a", {href: "#"}, playlist.name)));
        });

        return (React.createElement("span", null, 
          React.createElement("h3", null, "Playlist"), 
          React.createElement("nav", {className: "navbar navbar-default", role: "navigation"}, 
            React.createElement("div", {className: "container-fluid"}, 

                React.createElement("ul", {className: "nav navbar-nav"}, 
                    React.createElement("li", {className: "dropdown"}, 
                        React.createElement("a", {href: "#", className: "dropdown-toggle", 'data-toggle': "dropdown"}, "Playlists ", React.createElement("span", {className: "caret"})), 

                        React.createElement("form", {className: "form-inline pull-right", role: "form"}, 
                            React.createElement("div", {className: "form-group"}, 
                              React.createElement("input", {onChange: this.handleSearch, type: "text", className: "form-control input-sm col-xs-2", id: "q", placeholder: "Search..."})
                            ), 
                            React.createElement("div", {className: "form-group"}, 
                                React.createElement("button", {type: "button", onClick: this.handleAddVideo, className: "btn btn-success"}, React.createElement("i", {className: "glyphicon glyphicon-plus"}), "Video")
                            )
                        ), 

                        React.createElement("ul", {className: "dropdown-menu", role: "menu"}, 
                            React.createElement("li", {className: "btn btn-success"}, React.createElement("a", {href: "#"}, "Add Playlist")), 
                            React.createElement("li", {className: "divider"}), 
                            playlistNodes
                        ), 
                        React.createElement("li", null, React.createElement("a", {href: "#"}, this.state.current_playlist.name))
                    )
                )

            )
          ), 
          React.createElement("div", {className: "draggable list-group"}, 
            React.createElement("p", null, "(", this.state.total_num_items, ") results"), 
            feedNodes
          )
        ));

    },
});

// render the Base set
// React.render(
//   <FeedView />,
//   document.getElementById('feed-list')
// );

React.render(
  React.createElement(PlaylistView, null),
  document.getElementById('playlist-feed-list')
);

React.render(
  React.createElement(FeedPreviewView, null),
  document.getElementById('feed-preview')
);

// render the collaborators
React.render(
  React.createElement(CollaboratorListView, null),
  document.getElementById('project-detail-collaborators')
);