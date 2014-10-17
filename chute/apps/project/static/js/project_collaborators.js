/** @jsx React.DOM */
/**
* Project collaborators
*
*/
var CollaboratorFormModal = React.createClass({displayName: 'CollaboratorFormModal',
    getInitialState: function () {
        return {
            'collaborator': {},
            'messages': [],
            'is_disabled': true,
            'show_name_fields': false,
        }
    },
    isAlreadyCollaborating: function ( email ) {
        var collaborators = this.props.collaborators;
        var is_collaborating = false;
        var colaborator = {'name': null};

        $.each(collaborators, function ( index, collab ) {
            if ( collab.email == email ) {
                is_collaborating = true;
                colaborator = collab;
                return false;
            }
        });

        return $.extend({}, {'is_collaborating': is_collaborating}, colaborator);
    },
    onCheckCollaboratorExists: function ( event ) {
        var self = this;
        var searchEvent;
        var email = this.refs.email.getDOMNode().value.trim();
        var is_collaborating, colaborator_name;
        var collab = this.isAlreadyCollaborating( email );

        if ( collab.is_collaborating === false ) {
            var form = $('<form data-parsley-validate/>');
            form.append($('<input type="email" data-parsley-required="true" data-parsley-type="email" value="{email}" />'.assign({'email': email})))

            if ( form.parsley().isValid() === true ) {

                clearTimeout( searchEvent );

                searchEvent = setTimeout( function () {
                    UserResource.list( {'email': email} ).defer().done(function ( data ) {
                        var show_name_fields = false;
                        if ( data.results.length === 0 ) {

                            self.setState({
                                'collaborator': {},
                                'messages': [{'message': 'Please provide additional details for {email} to continue.'.assign({'email': email}), 'type': 'success'}],
                                'show_name_fields': true,
                                'is_disabled': false,
                            });
    
                        } else {
                            var collab = data.results[0];
                            self.setState({
                                'collaborator': collab,
                                'messages': [{'message': '{colaborator_name} can be added as a collaborator'.assign({'colaborator_name': collab.name}), 'type': 'success'}],
                                'show_name_fields': false,
                                'is_disabled': false,
                            });
                        }
                    });
                }, 900 );
            }

            self.setState({
                'messages': [],
                'show_name_fields': false,
                'is_disabled': true
            });

        } else {
            self.setState({
                'collaborator': {},
                'messages': [{'message': '{colaborator_name} is already a collaborator'.assign({'colaborator_name': collab.name}), 'type': 'warning'}],
            });
        } // end if is_collaborating
    },
    onSubmitForm: function ( event ) {
        event.preventDefault();
        var self = this;

        if ( $(event.target).parsley().isValid() === true ) {

            var email = this.refs.email.getDOMNode().value.trim();
            var first_name = this.refs.first_name.getDOMNode().value.trim();
            var last_name = this.refs.last_name.getDOMNode().value.trim();

            CollaboratorResource.create( email, first_name, last_name ).defer().done(function ( data ) {

                $( '#modal-new-collaborator' ).modal('hide');
                //document.location = video_data.video_url;
                //document.location.reload();
                self.props.onUpdateCollaborators( data );

            });
        }
        return false;
    },
    render: function () {

        var messagesView = Messages({messages: this.state.messages})
        var disabled = (this.state.is_disabled === true) ? 'disabled' : '' ;
        var showFieldsClass = (this.state.show_name_fields === true) ? '' : 'hide';


        return (React.DOM.div({id: "modal-new-collaborator", className: "modal fade bs-example-modal-lg", tabIndex: "-1", role: "dialog", 'aria-labelledby': "modal-new-collaborator-help", 'aria-hidden': "true"}, 
          React.DOM.div({className: "modal-dialog modal-lg"}, 
            React.DOM.div({className: "modal-content"}, 
                React.DOM.div({className: "modal-header"}, 
                    React.DOM.button({type: "button", className: "close", 'data-dismiss': "modal"}, React.DOM.span({'aria-hidden': "true"}, "×"), React.DOM.span({className: "sr-only"}, "Close")), 
                    React.DOM.h4({className: "modal-title", id: "myModalLabel"}, "New Collaborator")
                ), 
                React.DOM.div({className: "modal-body"}, 
                    React.DOM.div({className: "row"}, 
                        messagesView, 
                        React.DOM.form({onSubmit: this.onSubmitForm, 'data-parsley-validate': true}, 
                        React.DOM.label({htmlFor: "id_email"}, "Email Address:"), React.DOM.input({ref: "email", onChange: this.onCheckCollaboratorExists, 'data-parsley-maxlength': "200", 'data-parsley-group': "basic", 'data-parsley-required': "true", 'data-parsley-required-message': "This field is required.", 'data-parsley-type': "email", 'data-parsley-type-url-message': "Enter a valid Email Address.", id: "id_email", maxlength: "200", name: "email", type: "email"}), 
                            React.DOM.div({className: showFieldsClass}, 
                                React.DOM.label({htmlFor: "id_first_name"}, "First name:"), 
                                    React.DOM.input({ref: "first_name", 'data-parsley-maxlength': "255", 'data-parsley-group': "details", 'data-parsley-required': "true", 'data-parsley-required-message': "This field is required.", id: "id_first_name", maxlength: "255", name: "first_name", type: "text", value: this.state.collaborator.first_name}), 
                                React.DOM.label({htmlFor: "id_last_name"}, "Last name:"), 
                                    React.DOM.input({ref: "last_name", 'data-parsley-maxlength': "255", 'data-parsley-group': "details", 'data-parsley-required': "true", 'data-parsley-required-message': "This field is required.", id: "id_last_name", maxlength: "255", name: "last_name", type: "text", value: this.state.collaborator.last_name})
                            ), 
                            React.DOM.input({type: "submit", value: "Add", disabled: disabled})
                        )
                    )
                )
            )
          )
        ));
    }
});

var CollaboratorDetailView = React.createClass({displayName: 'CollaboratorDetailView',
    onDeleteCollaborator: function ( email, event ) {
        var self = this;
        CollaboratorResource.destroy( email ).defer().done(function ( data ) {

            self.props.onUpdateCollaborators( data );

        });
    },
    render: function () {
        var user_class = this.props.person.user_class
        var classNames = 'pull-right label';
        var deleteCss = 'pull-right';
        if ( user_class === 'owner' ) {
            classNames += ' label-primary';
            deleteCss = 'hide'; // dony allow user to delete the owner

        } else if (  user_class === 'colleague'  ) {
            classNames += ' label-info';

        } else {
            classNames += ' label-success';

        }
        return (
            React.DOM.li({key: this.props.person.pk, className: "list-group-item"}, 
            React.DOM.span({className: "glyphicon glyphicon-comment"}), " ", this.props.person.name, ":", 
            React.DOM.span({className: deleteCss}, " ", React.DOM.a({href: "javscript:;", onClick: this.onDeleteCollaborator.bind( this, this.props.person.email)}, React.DOM.span({className: "glyphicon glyphicon-remove"}))), 
            React.DOM.span({className: classNames}, this.props.person.user_class)
            )
        );
    }
});


var CollaboratorView = React.createClass({displayName: 'CollaboratorView',
    render: function () {
        var name = this.props.name;
        return (
            React.DOM.span(null, 
            React.DOM.span({className: "glyphicon glyphicon-comment"}), " ", name, ":"
            )
        )
    }
});


var CollaboratorListView = React.createClass({displayName: 'CollaboratorListView',
    getInitialState: function () {
        return {
            'collaborators': Project.collaborators,
        }
    },
    updateCollaborators: function ( collaborators ) {
        this.setState({'collaborators': collaborators});
    },
    render: function () {
        var self = this;
        var collaboratorFormModal = CollaboratorFormModal({collaborators: this.state.collaborators, 
                                                           onUpdateCollaborators: this.updateCollaborators})
        var collaboratorNodes = this.state.collaborators.map(function ( person ) {
            return CollaboratorDetailView({key: person.pk, 
                                           onUpdateCollaborators: self.updateCollaborators, 
                                           person: person})
        });

        return (
            React.DOM.span(null, 
              React.DOM.h2(null, "Collaborators"), 
              React.DOM.p(null, React.DOM.a({href: "#", className: "btn btn-success", 'data-toggle': "modal", 'data-target': "#modal-new-collaborator"}, "New Collaborator")), 
              React.DOM.ul({className: "list-group"}, 
                collaboratorNodes
              ), 
              collaboratorFormModal
            )
        );
    }
});