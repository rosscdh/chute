'use strict';
/*
2014. Ross Crawford-d'Heureuse to be a jquery.plugin
*/
$(function() {

    function UninitializedObjectException(message) {
       this.message = message;
       this.name = "UserException";
    }

    $.widget( "chute.chute_controller", {
        // default options
        timer: undefined,
        wait_for: undefined,
        template: undefined,
        current_feeditem: undefined,

        options: {
            'feed': undefined,
            'project': undefined,
            'templates': undefined,
            'renderer': Handlebars || undefined,

            'target': $('div#content'),

            'DEBUG': true,                              // -- show debug messages
        },

        log: function (msg) {
            var self = this;
            if (self.options.DEBUG === true) {
                console.log(msg)
            }
        },
        // the constructor
        _create: function() {
            var self = this;

            if ( this.options.feed === undefined ) {
                throw new UninitializedObjectException("You need to initialize the chute_controller");
            }

            self.current_feeditem = this.options.feed[0];
            self.wait_for = self.current_feeditem.wait_for;
            self.template = self.current_feeditem.template;

            this._listen();
            this._begin();
        },
        _listen: function () {
            var self = this;
            // setup pusher.com listeners and updaters here

        },
        timeout: function () {
            var timeout_in = (this.wait_for * 1000)
            this.log('Timeout set to: ' + timeout_in);
            return timeout_in;
        },
        _timer: function () {
            var self = this;
            if ( self.timer !== undefined ) {
                // the main timer object
                window.clearTimeout( self.timer );
            }
            // ensure we have more than 1 item in the feed for the rotator
            if ( self.options.feed.length > 1 ) {

                self.timer = window.setTimeout( function () {
                    // when it expires call next
                    self.next();
                }, self.timeout());

            }
        },
        _begin: function () {
            var self = this;

            // setup window setTime and window.clearTimer handler
            var source = this.options.templates[self.template];
            
            self.render( source );
            self._timer();
        },
        render: function ( source ) {
            var self = this;
            var target = self.options.target;
            var compiled = self.options.renderer.compile( source );
            var context = {
                'project': this.project,
                'object': this.current_feeditem,
        };
            target.html( compiled( context ) );
        },
        next: function () {
            var self = this;
            var next_item = null;

            this.log('Loading next') ;

            $.each(this.options.feed, function ( i, feed_item ) {

                self.log('Check for current and get next: ' + i +'');
                self.log('Current iteration PKs: feed_item:'+ feed_item.pk +' current_feeditem: '+ self.current_feeditem.pk);

                if ( feed_item.pk === self.current_feeditem.pk ) {
                    var next = parseInt(i + 1);

                    try {
                       next_item = self.options.feed[ next ];
                       console.log('i+1: '+ next)
                       self.log('next_item set to: ' + next_item.pk);
                    }
                    catch (e) {
                       // error occurred assume index error for now and set to 0
                       // for loop
                       next_item = self.options.feed[0];
                       self.log('Error: next_item set to index 0: ' + next_item + ' error: ' + e.message);
                    }

                    self.current_feeditem = next_item;

                    self.template = next_item.template;
                    self.log('Template set to: ' + next_item.template);

                    self.wait_for = next_item.wait_for;
                    self.log('Wait_for set to: ' + next_item.wait_for);

                    self.render( self.options.templates[self.template] );
                    self._timer();

                    return false;
                }
            });

        }
    });
});