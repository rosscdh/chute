/** @jsx React.DOM */
/**
* Project List
*
*/

var FlashMessageView = React.createClass({
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
            <div className={blockClassName} role="alert">
                {this.state.message}
            </div>
        );
    }
});


var ProjectItem = React.createClass({
  render: function() {

    return (
            <article className="col-md-4 project">
                <div className="card">

                    { this.props.editMatterInterface }

                    <a href={ this.props.detail_url } title={ this.props.name } className="content">
                        <div className="title">
                            <h6>{ this.props.project.client.name }</h6>
                            <h5>{ this.props.name }</h5>
                            { this.props.currentUserRole }
                        </div>
                        <div className="meta clearfix">
                            { this.props.lastupdated_or_complete }
                            { this.props.participantList }
                        </div>
                    </a>
                    <div className="progress">
                        <div className="progress-bar" style={ this.props.percentStyle }></div>
                    </div>
                </div>
            </article>
    );
  }
});

var Participants = React.createClass({
    render: function() {
        if (this.props.data.length > 3) {
            var userNames = this.props.data.map(function(user) {
                return user.name;
            });

            return (
                <div className="people people-multi pull-right" data-toggle="tooltip" title={userNames}>
                    <div className="avatar img-circle one">
                        <span className="initials">{this.props.data.length}</span>
                    </div>
                    <div className="avatar img-circle two"><span className="initials">&nbsp;</span></div>
                    <div className="avatar img-circle three"><span className="initials">&nbsp;</span></div>
                </div>
            );
        } else {
            var userNodes = this.props.data.map(function(user) {
                return (
                    <div className="avatar img-circle">
                        <span className="initials" title={user.name}>{user.initials}</span>
                    </div>
                )
            });

            return (
                <div className="people pull-right">
                    {userNodes}
                </div>
            );
        }
    }
});


var EditMatterInterface = React.createClass({
    render: function() {
        var key = this.props.key;
        var can_edit = this.props.can_edit;
        var edit_url = this.props.edit_url;
        var modal_target = '#project-edit-' + key;
        if (can_edit === true) {

            return (
                <a href={edit_url} data-toggle="modal" data-target={modal_target} className="edit btn-sm">
                    <span className="fui-gear" data-toggle="tooltip" data-placement="left" title="Edit Matter Details"></span>
                </a>
            );

        } else {

            return (<span/>);
        }
    }
});


var NoResultsInterface = React.createClass({
    render: function() {
        return (
            <div className="col-md-12 text-center">
                <h6 className="text-muted">No projects found</h6>
            </div>
        );
    },
});


var CreateMatterButton = React.createClass({
    render: function() {
        return (
            <a data-toggle="modal" data-target="#modal-project-create" className="btn btn-success btn-embossed pull-right"><i className="fui-plus"></i> New Project</a>
        );
    },
});


var ProjectList = React.createClass({
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
        var flashMessage = <FlashMessageView />
        var createButton = null;
        if (this.state.can_create) {
            createButton = <CreateMatterButton create_url={Links.create_url}/>
        }

        if ( this.state.total_num_projects == 0 ) {
            projectNodes = <NoResultsInterface />
        } else {
            projectNodes = this.state.projects.map(function (project) {
                var editUrl = Links.edit_url;
                var detailUrl = project.detail_url;

                var percentStyle = {'width': project.percent_complete};
                var client_name = project.client.name;

                var participantList = <Participants data={project.collaborators} />

                var editMatterInterface = <EditMatterInterface key={project.slug} can_edit={User.can_edit} edit_url={editUrl} />

                return <ProjectItem
                        key={project.slug}
                        name={project.name}
                        project={project}
                        participantList={participantList}
                        editMatterInterface={editMatterInterface}

                        export_info={project.export_info}

                        percent_complete={project.percent_complete}
                        percentStyle={percentStyle}
                        detail_url={detailUrl}
                        edit_url={editUrl}>{project}</ProjectItem>
            });
        }
        return (
            <section className="projects cards">
                <header className="page-header">
                    <h2>All Projects</h2>
                </header>
                <div className="row">
                    {createButton}
                    <br/><br/>
                    <div className="form-group">
                        <div className="input-group col-xs-12 search-field">
                            <input type="text" className="form-control" placeholder="Search projects by name or client name..." name="q" autocomplete="off" onChange={this.handleSearch} />
                        </div>
                    </div>
                </div>
                <div className="row">
                    {flashMessage}
                    {projectNodes}
                </div>
            </section>
        );
    }
});

React.renderComponent(
  <ProjectList />,
  document.getElementById('project-list')
);
