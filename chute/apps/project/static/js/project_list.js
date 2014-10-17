/** @jsx React.DOM */
/**
* Project List
*
*/

var FlashMessageView = React.createClass({displayName: 'FlashMessageView',
    getInitialState: function() {
        return {
                'message': null,
        }
    },
    handleFlashMessage: function (event) {
        console.log(event)
        this.setState({
            'message': event.message
        });
    },
    componentDidMount: function() {
        var self = this;
        $( "body" ).on( "alert_message", function( event ) {
            self.handleFlashMessage( event );
        });
    },
    render: function () {
        blockClassName = (this.state.message !== null) ? 'alert alert-warning fade in' : 'hide' ;
        return (
            React.DOM.div({className: blockClassName, role: "alert"}, 
                this.state.message
            )
        );
    }
});


var ProjectItem = React.createClass({displayName: 'ProjectItem',
  render: function() {

    return (
            React.DOM.article({className: "col-md-4 project"}, 
                React.DOM.div({className: "card"}, 

                     this.props.editMatterInterface, 

                    React.DOM.a({href:  this.props.detail_url, title:  this.props.name, className: "content"}, 
                        React.DOM.div({className: "title"}, 
                            React.DOM.h6(null,  this.props.project.client.name), 
                            React.DOM.h5(null,  this.props.name), 
                             this.props.currentUserRole
                        ), 
                        React.DOM.div({className: "meta clearfix"}, 
                             this.props.lastupdated_or_complete, 
                             this.props.participantList
                        )
                    ), 
                    React.DOM.div({className: "progress"}, 
                        React.DOM.div({className: "progress-bar", style:  this.props.percentStyle})
                    )
                )
            )
    );
  }
});

var Participants = React.createClass({displayName: 'Participants',
    render: function() {
        if (this.props.data.length > 3) {
            var userNames = this.props.data.map(function(user) {
                return user.name;
            });

            return (
                React.DOM.div({className: "people people-multi pull-right", 'data-toggle': "tooltip", title: userNames}, 
                    React.DOM.div({className: "avatar img-circle one"}, 
                        React.DOM.span({className: "initials"}, this.props.data.length)
                    ), 
                    React.DOM.div({className: "avatar img-circle two"}, React.DOM.span({className: "initials"}, " ")), 
                    React.DOM.div({className: "avatar img-circle three"}, React.DOM.span({className: "initials"}, " "))
                )
            );
        } else {
            var userNodes = this.props.data.map(function(user) {
                return (
                    React.DOM.div({className: "avatar img-circle"}, 
                        React.DOM.span({className: "initials", title: user.name}, user.initials)
                    )
                )
            });

            return (
                React.DOM.div({className: "people pull-right"}, 
                    userNodes
                )
            );
        }
    }
});


var EditMatterInterface = React.createClass({displayName: 'EditMatterInterface',
    render: function() {
        var key = this.props.key;
        var can_edit = this.props.can_edit;
        var edit_url = this.props.edit_url;
        var modal_target = '#project-edit-' + key;
        if (can_edit === true) {

            return (
                React.DOM.a({href: edit_url, 'data-toggle': "modal", 'data-target': modal_target, className: "edit btn-sm"}, 
                    React.DOM.span({className: "fui-gear", 'data-toggle': "tooltip", 'data-placement': "left", title: "Edit Matter Details"})
                )
            );

        } else {

            return (React.DOM.span(null));
        }
    }
});


var NoResultsInterface = React.createClass({displayName: 'NoResultsInterface',
    render: function() {
        return (
            React.DOM.div({className: "col-md-12 text-center"}, 
                React.DOM.h6({className: "text-muted"}, "No projects found")
            )
        );
    },
});


var CreateMatterButton = React.createClass({displayName: 'CreateMatterButton',
    render: function() {
        return (
            React.DOM.a({'data-toggle': "modal", 'data-target': "#modal-project-create", className: "btn btn-success btn-embossed pull-right"}, React.DOM.i({className: "fui-plus"}), " New Project")
        );
    },
});


var ProjectList = React.createClass({displayName: 'ProjectList',
    fuse: new Fuse(Projects, { keys: ["name", "client.name"], threshold: 0.35 }),
    getInitialState: function() {
        return {
            'can_create': true,
            'projects': Projects,
            'total_num_projects': Projects.length
        }
    },
    handleSearch: function(event) {
        var searchFor = event.target.value;
        var project_list_results = (searchFor != '') ? this.fuse.search(event.target.value) : Projects

        this.setState({
            projects: project_list_results,
            total_num_projects: project_list_results.length,
            searched: true
        });
    },
    render: function() {
        var projectNodes = null;
        var flashMessage = FlashMessageView(null)
        var createButton = null;
        if (this.state.can_create) {
            createButton = CreateMatterButton({create_url: Links.create_url})
        }

        if ( this.state.total_num_projects == 0 ) {
            projectNodes = NoResultsInterface(null)
        } else {
            projectNodes = this.state.projects.map(function (project) {
                var editUrl = Links.edit_url;
                var detailUrl = project.detail_url;

                var percentStyle = {'width': project.percent_complete};
                var client_name = project.client.name;

                var participantList = Participants({data: project.collaborators})

                var editMatterInterface = EditMatterInterface({key: project.slug, can_edit: User.can_edit, edit_url: editUrl})

                return ProjectItem({
                        key: project.slug, 
                        name: project.name, 
                        project: project, 
                        participantList: participantList, 
                        editMatterInterface: editMatterInterface, 

                        export_info: project.export_info, 

                        percent_complete: project.percent_complete, 
                        percentStyle: percentStyle, 
                        detail_url: detailUrl, 
                        edit_url: editUrl}, project)
            });
        }
        return (
            React.DOM.section({className: "projects cards"}, 
                React.DOM.header({className: "page-header"}, 
                    React.DOM.h2(null, "All Projects")
                ), 
                React.DOM.div({className: "row"}, 
                    createButton, 
                    React.DOM.br(null), React.DOM.br(null), 
                    React.DOM.div({className: "form-group"}, 
                        React.DOM.div({className: "input-group col-xs-12 search-field"}, 
                            React.DOM.input({type: "text", className: "form-control", placeholder: "Search projects by name or client name...", name: "q", autocomplete: "off", onChange: this.handleSearch})
                        )
                    )
                ), 
                React.DOM.div({className: "row"}, 
                    flashMessage, 
                    projectNodes
                )
            )
        );
    }
});

React.renderComponent(
  ProjectList(null),
  document.getElementById('project-list')
);
