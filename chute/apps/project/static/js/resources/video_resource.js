'use strict';


var VideoResource = Resource.createClass({
    uri: '/api/v1/videos/',
    base_url: function ( params ) {
        return this.uri + '{video_slug}/'.assign(params || this.params);
    },
    create: function ( post_params ) {
        return this.process( this.uri, 'POST', post_params );
    },
    detail: function ( params ) {
        var uri = this.base_url( params );
        return this.process( uri, 'GET' );
    },
    destroy: function ( pk ) {
        var uri = this.base_url({video_slug: pk });
        return this.process( uri, 'DELETE', {'is_deleted': true});
    },
});
