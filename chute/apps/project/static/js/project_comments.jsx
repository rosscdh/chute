/** @jsx React.DOM */
/**
* Shared Project Comments objects
*
*/
// collaborators view
// comment list view
var CollaboratorsView = React.createClass({
    render: function () {
        return (<span/>);
    }
});

// Comment form
var CommentFormView = React.createClass({
    getInitialState: function () {
        return {
            'comment': '',
            'available_types': ['Comment', 'Subtitle', 'Sketch']
        }
    },
    handleSubmitComment: function ( event ) {
        event.preventDefault();
        var self = this;

        var comment = this.refs.comment.getDOMNode().value.trim();
        var comment_type = this.refs.comment_type.getDOMNode().value.trim();
        var comment_by = User.initials;
        var progress = this.props.progress;

        CommentResource.create( comment, comment_type, comment_by, progress ).defer().done(function ( data ) {

            VideoResource.detail( {video_slug: Video.slug} ).defer().done(function ( data ) {

                self.refs.comment.getDOMNode().value = '';
                self.props.onVideoUpdate( data );
            });

        });
        return false;
    },
    render: function () {
        var self = this;
        var is_link = false;
        var current_type = this.props.current_type.toLowerCase();
        var commentTypeNodes = this.state.available_types.map(function ( type, index ) {
            return (<li key={index}>
                <a href="javascript:;" onClick={self.props.onSetCurrentType}>{type}</a>
            </li>);
        });
        var Timestamp = <TimestampView is_link={is_link} progress={this.props.progress} />
        // be more clver with this turn into an array and then push and join at end
        var btnClassNameA = 'btn';
        var btnClassNameB = 'btn dropdown-toggle';

        if ( current_type == 'comment' ) {
            btnClassNameA += ' btn-success';
            btnClassNameB += ' btn-success';

        } else if ( current_type == 'subtitle' ) {    
            btnClassNameA += ' btn-warning';
            btnClassNameB += ' btn-warning';

        } else {
            btnClassNameA += ' btn-info';
            btnClassNameB += ' btn-info';
        }

        return (
            <form ref="" onSubmit={this.handleSubmitComment} className="text-center">
                {Timestamp}

                <div className="input-group">
                    <span className="input-group-addon">
                        <div className="control-type-selector btn-group">
                          <button type="button" className={btnClassNameA}>{this.props.current_type}</button>
                          <button type="button" className={btnClassNameB} data-toggle="dropdown">
                            <span className="caret"></span>
                            <span className="sr-only">Toggle Dropdown</span>
                          </button>
                          <ul className="dropdown-menu" role="menu">
                            {commentTypeNodes}
                          </ul>
                        </div>
                    </span>
                    <textarea ref="comment" name="comment" placeholder="Add comment here..." className="form-control input-lg" />
                    <input type="hidden" ref="comment_type" value={current_type} />
                    <span className="input-group-addon"><input className="btn btn-primary" type="submit" value="send" /></span>
                </div>
                <small>*supports markdown</small>
            </form>
        );
    }
});

var SubtitleForm = React.createClass({
    getInitialState: function () {
        console.log(this.props.comment.secs + 'HERE')
        return {
            'secs': this.props.comment.secs || 4
        }
    },
    handleSubmit: function ( event ) {
        event.preventDefault();
        var self = this;

        var comment_pk = this.props.comment.pk;
        var data = {
            'secs': parseInt(this.refs.secs.getDOMNode().value.trim()),
        };

        CommentResource.update( comment_pk, data ).defer().done(function ( data ) {
            console.log(data)
        });
        return false;
    },
    render: function () {
        return (<form  data-parsley-validate>
            <div className="input-group">
                <label htmlFor="">Show for:</label>
                <input type="input" ref="secs" onChange={this.handleSubmit} defaultValue={this.state.secs} data-parsley-group="subtitle-form" data-parsley-required="true" data-parsley-type="integer" />
                <span class="input-group-addon">secs</span>
            </div>
        </form>);
    }
});

var CommentItemView = React.createClass({
    handleDeleteComment: function ( pk, event ) {
        var self = this;

        CommentResource.destroy( pk ).defer().done(function ( data ) {

            if ( data.status_text === undefined ) {
                VideoResource.detail().defer().done(function ( data ) {
                    self.props.onVideoUpdate( data );
                });
            }

        });
    },
    form: function ( comment ) {
        var comment_type = comment.comment_type.toLowerCase();

        if ( this.props.show_form === false ) {
            return null;
        }

        if ( comment_type === 'comment' ) {
            return null;

        } else if ( comment_type === 'sketch' ) {
            return null;

        } else {
            // subtitle
            return <SubtitleForm comment={this.props.comment} />
        }

        return null;
    },
    render: function () {
        var comment = this.props.comment;
        // markdownify the comment
        comment_markdown = this.props.markdown_converter.makeHtml(comment.comment);
        var comment_type = comment.comment_type.toLowerCase();
        var collaborator = <CollaboratorView name={comment.comment_by} />
        var timestamp = <TimestampView onSeekTo={this.props.onSeekTo} progress={comment.progress}/>
        var date_of = moment(comment.date_of).fromNow();
        var type_className = 'label label-warning';
        var form = this.form(comment);

        if ( comment_type === 'comment' ) {
            type_className = 'label label-success';

        } else if ( comment_type === 'sketch' ) {
            type_className = 'label label-info';
        }

        return (
            <li key={comment.uuid} className="row">
                
                <div className="col-xs-3 pull-right">
                    <a href="javascript:;" onClick={this.handleDeleteComment.bind( this, comment.pk )}><span className="glyphicon glyphicon-remove-circle pull-right"></span></a>
                    <br/><span className="pull-right">{timestamp}</span>
                    <br/><span className="pull-right"><small>{date_of}</small></span>
                </div>

                <span className={type_className}>{comment_type}</span>

                <blockquote>
                    {collaborator}&nbsp;
                    <span dangerouslySetInnerHTML={{__html: comment_markdown}} />
                </blockquote>
                {form}
            </li>
        )
    }
});

// comment list view
var CommentListView = React.createClass({
    render: function () {
        var self = this;
        var markdown_converter = new Showdown.converter();
        var show_comment_form = (this.props.show_form !== undefined) ? this.props.show_form : true;

        var commentNodes = this.props.comments.map(function (comment) {
            return <CommentItemView key={comment.pk}
                                    markdown_converter={markdown_converter}
                                    show_form={show_comment_form}
                                    onVideoUpdate={self.props.onVideoUpdate}
                                    onSeekTo={self.props.onSeekTo}
                                    comment={comment} />
        });
        console.log(commentNodes.length)
        return (<span>
        <ul className="list-unstyled list-group">
            {commentNodes}
        </ul>
        </span>);
    }
});
