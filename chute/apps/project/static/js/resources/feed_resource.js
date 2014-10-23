'use strict';


var FeedItemResource = Resource.createClass({
    uri: '/api/v1/feed/',
    base_url: function ( params ) {
        return this.uri + '{pk}/'.assign(params || this.params);
    },
    create: function ( form_data ) {
        return this.process( this.uri, 'POST', form_data, 'html' );
    },
    update: function ( pk, kwargs ) {
        var uri = this.base_url({'pk': pk});
        return this.process( uri, 'PATCH', kwargs );
    },
    detail: function ( pk ) {
        var uri = this.base_url({'pk': pk });
        return this.process( uri, 'GET' );
    },
});
