'use strict';

var Resource = {
  uri: '/api/v1/',
  params: {},
  createClass: function ( options ) {
    return $.extend({}, this, options);
  },
  base_url: function () {
    return '/api/v1/'
  },
  process: function (url, method, data) {
    var self = this;

    this._promise = $.ajax({
                        dataType: 'json',
                        type: method,
                        url: url,
                        data: data,
                        headers: {
                            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                        }
                    });

    return this;
  },
  list: function () {
    return null;
  },
  create: function () {
    return null;
  },
  detail: function () {
    return null;
  },
  update: function () {
    return null;
  },
  destroy: function () {
    return null;
  },
  defer: function () {

    return this._promise.done( function ( data ) {
        if ( data === undefined ) {
          return {};
        }

        if ( data.responseText === undefined ) {

            return data;

        } else {
            return {
                'message': data.responseText,
                'status': data.status,
                'status_text': data.statusText
            };
        }
    });

  }
};
