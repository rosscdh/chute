'use strict';


var CollaboratorResource = Resource.createClass({
    uri: '/api/v1/projects/{slug}/collaborators/',
    base_url: function ( params ) {
        return this.uri.assign(params || this.params);
    },
    list: function () {
        return this.process( this.base_url(), 'GET' );
    },
    create: function ( email, first_name, last_name ) {
        var post_params = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        };
        return this.process( this.base_url(), 'POST', post_params );
    },
    detail: function ( email ) {
        var uri = '{base_url}{email}'.assign({'base_url': this.base_url(), 'email': email});
        return this.process( uri, 'GET' );
    },
    destroy: function ( email ) {
        var uri = '{base_url}{email}'.assign({'base_url': this.base_url(), 'email': email});
        return this.process( uri, 'DELETE' );
    },
});
