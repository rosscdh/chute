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
        var blockClassName = (this.state.message !== null) ? 'alert alert-warning fade in' : 'hide' ;
        return (
            React.createElement("div", {className: blockClassName, role: "alert"}, 
                this.state.message
            )
        );
    }
});


var ProjectItem = React.createClass({displayName: 'ProjectItem',
  render: function() {

    return (
            React.createElement("article", {className: "col-md-4 project"}, 
                React.createElement("div", {className: "card"}, 

                     this.props.editMatterInterface, 

                    React.createElement("a", {href:  this.props.detail_url, title:  this.props.name, className: "content"}, 
                        React.createElement("div", {className: "title"}, 
                            React.createElement("h6", null,  this.props.project.client.name), 
                            React.createElement("h5", null,  this.props.name), 
                             this.props.currentUserRole
                        ), 
                        React.createElement("div", {className: "meta clearfix"}, 
                             this.props.lastupdated_or_complete, 
                             this.props.participantList
                        )
                    ), 
                    React.createElement("div", {className: "progress"}, 
                        React.createElement("div", {className: "progress-bar", style:  this.props.percentStyle})
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
                React.createElement("div", {className: "people people-multi pull-right", 'data-toggle': "tooltip", title: userNames}, 
                    React.createElement("div", {className: "avatar img-circle one"}, 
                        React.createElement("span", {className: "initials"}, this.props.data.length)
                    ), 
                    React.createElement("div", {className: "avatar img-circle two"}, React.createElement("span", {className: "initials"}, " ")), 
                    React.createElement("div", {className: "avatar img-circle three"}, React.createElement("span", {className: "initials"}, " "))
                )
            );
        } else {
            var userNodes = this.props.data.map(function(user) {
                return (
                    React.createElement("div", {className: "avatar img-circle"}, 
                        React.createElement("span", {className: "initials", title: user.name}, user.initials)
                    )
                )
            });

            return (
                React.createElement("div", {className: "people pull-right"}, 
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
                React.createElement("a", {href: edit_url, 'data-toggle': "modal", 'data-target': modal_target, className: "edit btn-sm"}, 
                    React.createElement("span", {className: "fui-gear", 'data-toggle': "tooltip", 'data-placement': "left", title: "Edit Matter Details"})
                )
            );

        } else {

            return (React.createElement("span", null));
        }
    }
});


var NoResultsInterface = React.createClass({displayName: 'NoResultsInterface',
    render: function() {
        return (
            React.createElement("div", {className: "col-md-12 text-center"}, 
                React.createElement("h6", {className: "text-muted"}, "No projects found")
            )
        );
    },
});


var CreateMatterButton = React.createClass({displayName: 'CreateMatterButton',
    render: function() {
        return (
            React.createElement("a", {'data-toggle': "modal", 'data-target': "#modal-project-create", className: "btn btn-success btn-embossed pull-right"}, React.createElement("i", {className: "fui-plus"}), " New Project")
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
        var flashMessage = React.createElement(FlashMessageView, null)
        var createButton = null;
        if (this.state.can_create) {
            createButton = React.createElement(CreateMatterButton, {create_url: Links.create_url})
        }

        if ( this.state.total_num_projects == 0 ) {
            projectNodes = React.createElement(NoResultsInterface, null)
        } else {
            projectNodes = this.state.projects.map(function (project) {
                var editUrl = Links.edit_url;
                var detailUrl = project.detail_url;

                var percentStyle = {'width': project.percent_complete};
                var client_name = project.client.name;

                var participantList = React.createElement(Participants, {data: project.collaborators})

                var editMatterInterface = React.createElement(EditMatterInterface, {key: project.slug, can_edit: User.can_edit, edit_url: editUrl})

                return React.createElement(ProjectItem, {
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
            React.createElement("section", {className: "projects cards"}, 
                React.createElement("header", {className: "page-header"}, 
                    React.createElement("h2", null, "All Projects")
                ), 
                React.createElement("div", {className: "row"}, 
                    createButton, 
                    React.createElement("br", null), React.createElement("br", null), 
                    React.createElement("div", {className: "form-group"}, 
                        React.createElement("div", {className: "input-group col-xs-12 search-field"}, 
                            React.createElement("input", {type: "text", className: "form-control", placeholder: "Search projects by name or client name...", name: "q", autoComplete: "off", onChange: this.handleSearch})
                        )
                    )
                ), 
                React.createElement("div", {className: "row"}, 
                    flashMessage, 
                    projectNodes
                )
            )
        );
    }
});

React.render(
  React.createElement(ProjectList, null),
  document.getElementById('project-list')
);
