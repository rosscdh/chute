'use strict';


var ProjectResource = Resource.createClass({
    uri: '/api/v1/projects/',
    base_url: function ( params ) {
        return uri + '{slug}/'.assign(params || this.params);
    },
    create: function ( form_data ) {
        return this.process( this.uri, 'POST', form_data, 'html' );
    },
    detail: function ( project_slug ) {
        var uri = this.base_url({'slug': project_slug });
        return this.process( uri, 'GET' );
    },
});

var ProjectFeedResource = Resource.createClass({
    uri: '/api/v1/projects/{slug}/feed/',
    base_url: function ( params ) {
        return this.uri.assign(params || this.params);
    },
    create: function ( form_data ) {
        var uri = this.base_url();
        return this.process( uri, 'POST', form_data );
    },
});

var ProjectPlaylistFeedResource = Resource.createClass({
    uri: '/api/v1/projects/{project_slug}/playlist/{pk}/',
    base_url: function ( params ) {
        var p = $.extend({}, params, this.params);
        return this.uri.assign( p );
    },
    create: function ( form_data, url_params ) {
        var uri = this.base_url( url_params || {} );
        return this.process( uri, 'POST', form_data );
    },
    destroy: function ( feeditem_pk, url_params ) {
        var uri = this.base_url( url_params || {} );
        uri = uri + '{feeditem_pk}/'.assign({'feeditem_pk': feeditem_pk });
        return this.process( uri, 'DELETE' );
    },
});