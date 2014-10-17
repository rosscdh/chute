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

var ProjectVideoResource = Resource.createClass({
    uri: '/api/v1/projects/{slug}/videos/upload/',
    base_url: function ( params ) {
        return this.uri.assign(params || this.params);
    },
    create: function ( form_data ) {
        var uri = this.base_url();
        return this.process( uri, 'POST', form_data );
    },
});