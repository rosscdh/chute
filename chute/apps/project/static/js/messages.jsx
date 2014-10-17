/** @jsx React.DOM */
/**
* Generic Messages holder
*
*/
var MessageItem = React.createClass({
    render: function () {

        var message = this.props.message;
        var rowClass = "alert alert-{type}".assign({'type': message.type || 'info'});

        return (<li role="alert" className={rowClass}>
            {message.message}
        </li>);
    }
});

var Messages = React.createClass({
    render: function () {
        var message_set = this.props.messages || [];
        var messages = message_set.map( function( message ) {
            return <MessageItem message={message} />;
        });

        showOrHideCss = (message_set.length > 0)? 'row messages col-xs-12 list-unstyled' : 'row messages col-xs-12 hide list-unstyled';

        return (<ul className={showOrHideCss}>
            {messages}
        </ul>);
    }
});