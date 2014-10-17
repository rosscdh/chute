'use strict';


var CommentResource = Resource.createClass({
  uri: '/api/v1/videos/',
  base_url: function () {
    return this.uri + '{video_slug}/comments/'.assign(this.params);
  },
  list: function () {
    var uri = this.base_url();
    return this.process( uri, 'GET' );
  },
  create: function ( comment, comment_type, comment_by, progress ) {
    var uri = this.base_url();
    return this.process( uri, 'POST', {'comment': comment, 'comment_type': comment_type, 'comment_by': comment_by, 'progress': progress} );
  },
  detail: function ( comment_pk ) {
    var uri = this.base_url() + comment_pk + '/';
    return this.process( uri, 'GET' );
  },
  update: function ( pk, kwargs ) {
    var uri = this.base_url() + pk + '/';
    return this.process( uri, 'PATCH', kwargs );
  },
  destroy: function ( comment_pk ) {
    var uri = this.base_url() + comment_pk + '/';
    return this.process( uri, 'DELETE', {'is_deleted': true});
  },
});
