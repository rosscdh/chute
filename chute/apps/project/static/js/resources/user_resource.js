'use strict';


var UserResource = Resource.createClass({
    uri: '/api/v1/users/',
    base_url: function ( params ) {
        return this.uri.assign(params || this.params);
    },
    list: function ( url_params ) {
        var params = '?' + $.param( url_params );
        return this.process( this.base_url() + params, 'GET' );
    }
});
